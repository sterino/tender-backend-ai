import json
import os
from datetime import datetime

import requests
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo.database import Database
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from ..utils.security import hash_password

load_dotenv()
token = os.getenv("EGZ_TOKEN")


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict, gosuser: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "bin": user["bin"],
            "nameRu": gosuser[0]["nameRu"],
            "pid": gosuser[0]["pid"],
            "regdate": gosuser[0]["regdate"],
            "gosemail": gosuser[0]["email"],
            "phone": gosuser[0]["phone"],
            "supplier": gosuser[0]["supplier"],
            "typeSupplier": gosuser[0]["typeSupplier"],
            "customer": gosuser[0]["customer"],
            "organizer": gosuser[0]["organizer"],
            "employers": {
                "employer": {
                    "roleName": emp["roleName"],
                    "iin": emp["iin"],
                    "fio": emp["fio"],
                }
                for emp in gosuser[0]["Employees"]
            },
            "Address": {"address": add["address"] for add in gosuser[0]["Address"]},
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )

    def get_user_by_bin(self, bin: str):
        disable_warnings(InsecureRequestWarning)

        info = bin
        url = "https://ows.goszakup.gov.kz/v3/graphql"

        # API token for authorization
        headers = {"Authorization": f"Bearer {token}"}

        # Query for searching by bin
        query_by_bin = """
                    query ($bin: String!) {
                        Subjects(filter: { bin: $bin }) {
                            nameRu
                            pid
                            bin
                            iin
                            inn
                            unp
                            regdate
                            email
                            phone
                            katoList
                            supplier
                            typeSupplier
                            customer
                            organizer
                            markNationalCompany
                            qvazi
                            Employees {
                                roleName
                                iin
                                fio
                            }
                            Address {
                                address
                            }
                        }
                    }
                """

        def make_graphql_request(query, variables):
            response = requests.post(
                url,
                json={"query": query, "variables": variables},
                headers=headers,
                verify=False,
            )
            data = json.loads(response.text)

            if "errors" in data:
                raise Exception(data["errors"][0]["message"])

            return data

            # Variables for the GraphQL query

        variables_by_bin = {"bin": info}

        response_by_bin = make_graphql_request(query_by_bin, variables_by_bin)
        subjects_by_bin = response_by_bin["data"]["Subjects"]
        if subjects_by_bin is not None:
            return subjects_by_bin
