import json
import os

import openai
import requests
from dotenv import load_dotenv
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

load_dotenv()
token = os.getenv("EGZ_TOKEN")


def getSubject(input: str):
    disable_warnings(InsecureRequestWarning)

    info = input
    url = "https://ows.goszakup.gov.kz/v3/graphql"

    # API token for authorization
    headers = {"Authorization": f"Bearer {token}"}

    # Query for searching by bin
    query_by_bin = """
                query ($bin: String!) {
                    Subjects(filter: { bin: $bin }, limit: 200) {
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

    # Query for searching by iin
    query_by_iin = """
                query ($iin: String!) {
                    Subjects(filter: { iin: $iin }, limit: 200) {
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

    query_by_name = """
                query ($nameOrFullNameRu: String!) {
                    Subjects(filter: { nameOrFullNameRu: $nameOrFullNameRu }, limit: 200) {
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

    # Function to make GraphQL request
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
    variables_by_iin = {"iin": info}
    varibales_by_name = {"nameOrFullNameRu": info}

    # Make the GraphQL requests
    response_by_bin = make_graphql_request(query_by_bin, variables_by_bin)
    subjects_by_bin = response_by_bin["data"]["Subjects"]
    if subjects_by_bin is not None:
        return subjects_by_bin
    response_by_iin = make_graphql_request(query_by_iin, variables_by_iin)
    subjects_by_iin = response_by_iin["data"]["Subjects"]
    if subjects_by_iin is not None:
        return subjects_by_iin
    response_by_name = make_graphql_request(query_by_name, varibales_by_name)
    subjects_by_name = response_by_name["data"]["Subjects"]
    if subjects_by_name is not None:
        return subjects_by_name


def getTrades(input):
    disable_warnings(InsecureRequestWarning)

    info = input
    url = "https://ows.goszakup.gov.kz/v3/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    # Query for searching by bin
    query = """
        query($nameRu: String!) {
            TrdBuy(filter: { nameRu: $nameRu }){
                id
                nameRu
                totalSum
                countLots
                refTradeMethodsId
                refSubjectTypeId
                customerBin
                kato
                customerNameRu
                orgBin
                orgNameRu
                refBuyStatusId
                startDate
                endDate
                repeatStartDate
                repeatEndDate
                itogiDatePublic
                refTypeTradeId
                disablePersonId
                discusStartDate
                discusEndDate
                idSupplier
                biinSupplier
                parentId
                Commission{
                    id
                    fio
                    refCommRolesId
                    bin
                }
                Lots{
                    id
                    refLotStatusId
                    count
                    amount
                    nameRu
                    descriptionRu
                    customerBin
                    customerNameRu
                    trdBuyId
                    plnPointKatoList
                    disablePersonId
                    Files{
                        id
                        filePath
                        nameRu
                        originalName
                    }
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

    variables = {"nameRu": f"*{info}*"}
    response = make_graphql_request(query, variables)
    Trade = response["data"]["TrdBuy"]
    return Trade


def getLots(input: str):
    disable_warnings(InsecureRequestWarning)
    info = input
    url = "https://ows.goszakup.gov.kz/v3/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    query = """
        query($nameRu: String!) {
            Lots(filter: { nameRu: $nameRu }){
                id
                refLotStatusId
                count
                amount
                nameRu
                descriptionRu
                customerBin
                customerNameRu
                trdBuyId
                plnPointKatoList
                disablePersonId
                Files{
                    id
                    filePath
                    nameRu
                    originalName
                }
                TrdBuy{
                    id
                    nameRu
                    totalSum
                    countLots
                    refTradeMethodsId
                    refSubjectTypeId
                    customerBin
                    kato
                    customerNameRu
                    orgBin
                    orgNameRu
                    refBuyStatusId
                    startDate
                    endDate
                    repeatStartDate
                    repeatEndDate
                    itogiDatePublic
                    refTypeTradeId
                    disablePersonId
                    discusStartDate
                    discusEndDate
                    idSupplier
                    biinSupplier
                    parentId
                    Commission{
                        id
                        fio
                        refCommRolesId
                        bin
                    }
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

    variables = {"nameRu": f"*{info}*"}
    response = make_graphql_request(query, variables)
    Trade = response["data"]["Lots"]
    return Trade


class ChatService:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def get_response(self, prompt):
        function_descriptions = [
            {
                "name": "getSubject",
                "description": "Call this function to find subjects or companies by biin or iin or name of company or subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "NameBinIin": {
                            "type": "string",
                            "description": "Text that will be used for search subjects by iin or biin or name of subject or company",
                        },
                    },
                    "required": ["NameBinIin"],
                },
            },
            {
                "name": "getTrades",
                "description": "Call this function to find trades or adverts or tenders",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "Text that will be used for search adverts and trades by description",
                        },
                    },
                    "required": ["description"],
                },
            },
            {
                "name": "getContracts",
                "description": "this function useful to find treaty or contracts by biin or iin or name of company or subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text_for_search": {
                            "type": "string",
                            "description": "Text that will be used for search contracts by biin or iin or name of company or subject",
                        },
                    },
                    "required": ["text_for_search"],
                },
            },
            {
                "name": "getActs",
                "description": "Call this function to find acts by biin or iin or name of company or subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text_for_search": {
                            "type": "string",
                            "description": "Text that will be used for search acts by biin or iin or name of company or subject",
                        },
                    },
                    "required": ["text_for_search"],
                },
            },
            {
                "name": "getLots",
                "description": "Call this function to find lots",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text_for_search": {
                            "type": "string",
                            "description": "Text that will be used for search lots by description",
                        },
                    },
                    "required": ["text_for_search"],
                },
            },
            {
                "name": "getTradesApp",
                "description": "call this function to search for user's trades orders by biin or iin or name of company or subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text_for_search": {
                            "type": "string",
                            "description": "Text that will be used for search user's trades orders by biin or iin or name of company or subject",
                        },
                    },
                    "required": ["text_for_search"],
                },
            },
            # {
            #     "name": "getRnu",
            #     "description": "Call this function to find the stupidest person",
            #     "parameters": {
            #         "type": "object",
            #         "properties": {
            #             "text_for_search": {
            #                 "type": "string",
            #                 "description": "input",
            #             },
            #         },
            #         "required": ["text_for_search"],
            #     },
            # },
            # {
            #     "name": "getPlans",
            #     "description": "Call this function to find the smart person",
            #     "parameters": {
            #         "type": "object",
            #         "properties": {
            #             "text_for_search": {
            #                 "type": "string",
            #                 "description": "input",
            #             },
            #         },
            #         "required": ["text_for_search"],
            #     },
            # },
        ]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": prompt}],
            functions=function_descriptions,
            function_call="auto",  # specify the function call
        )

        output = completion.choices[0].message
        # input = output.function_call.arguments.NameBinIin
        params = output.function_call.name
        print(params)

        if params == "getSubject":
            arguments = output.function_call.arguments
            argument = json.loads(arguments)
            inp = argument.get("NameBinIin", "")
            print(inp)
            result = getSubject(inp)
            return 1, result
        elif params == "getTrades":
            arguments = output.function_call.arguments
            argument = json.loads(arguments)
            inp = argument.get("description", "")
            # strKato = argument.get("strKato", "")
            print(inp)
            result = getTrades(inp)
            return 5, result
        elif params == "getLots":
            arguments = output.function_call.arguments
            argument = json.loads(arguments)
            inp = argument.get("text_for_search", "")
            # strKato = argument.get("strKato", "")
            print(inp)
            result = getLots(inp)
            return 6, result
        elif params == "getTradesApp":
            arguments = output.function_call.arguments
            argument = json.loads(arguments)
            inp = argument.get("text_for_search", "")
            # strKato = argument.get("strKato", "")
            result = getSubject(inp)
            return 4, result
        elif params == "getContracts":
            arguments = output.function_call.arguments
            argument = json.loads(arguments)
            inp = argument.get("text_for_search", "")
            # strKato = argument.get("strKato", "")
            print(inp)
            result = getSubject(inp)
            return 2, result
        elif params == "getActs":
            arguments = output.function_call.arguments
            argument = json.loads(arguments)
            inp = argument.get("text_for_search", "")
            # strKato = argument.get("strKato", "")
            print(inp)
            result = getSubject(inp)
            return 3, result
