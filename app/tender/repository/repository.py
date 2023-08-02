import json
import os

import requests
from dotenv import load_dotenv
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

load_dotenv()
token = os.getenv("EGZ_TOKEN")


class tenderRepository:
    # Функция для получения актов
    def getActs(self, input: str):
        disable_warnings(InsecureRequestWarning)

        info = int(input)
        url = "https://ows.goszakup.gov.kz/v3/graphql"
        headers = {"Authorization": f"Bearer {token}"}

        # Query for searching by bin
        query_by_supplier = """
            query($supplierId: Int!) {
                Acts(filter: { supplierId: $supplierId },  limit: 200){
                    id
                    aktDate
                    approveDate
                    revokeDate
                    createDateAct
                    statusId
                    dayOverdue
                    sumAvans
                    sumBeginning
                    sumFine
                    sumPreviously
                    statusNameRu
                    typeAct
                    File{
                        nameRu
                        filePath
                    }
                    Supplier{
                        nameRu
                    }
                }
            }
        """
        query_by_customer = """
            query($supplierId: Int!, $id: Int!) {
                Acts(filter: { supplierId: $supplierId }, limit: 200){
                    id
                    aktDate
                    approveDate
                    revokeDate
                    createDateAct
                    statusId
                    dayOverdue
                    sumAvans
                    sumBeginning
                    sumFine
                    sumPreviously
                    statusNameRu
                    typeAct
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

        variables_by_supplier = {"supplierId": info}
        variables_by_customer = {"customerId": info}

        response_by_supplier = make_graphql_request(
            query_by_supplier, variables_by_supplier
        )
        act_by_supplier = response_by_supplier["data"]["Acts"]
        if act_by_supplier is not None:
            return act_by_supplier
        response_by_customer = make_graphql_request(
            query_by_customer, variables_by_customer
        )
        act_by_customer = response_by_customer["data"]["Acts"]
        if act_by_customer is not None:
            return act_by_customer

    def getContracts(self, input: str):
        disable_warnings(InsecureRequestWarning)

        info = input
        url = "https://ows.goszakup.gov.kz/v3/graphql"
        headers = {"Authorization": f"Bearer {token}"}

        # Query for searching by bin
        query_by_supplier = """
            query($supplierBiin: String!) {
                Contract(filter: { supplierBiin: $supplierBiin }, limit: 200){
                    id
                    parentId
                    trdBuyId
                    trdBuyNumberAnno
                    trdBuyNameRu
                    refContractStatusId
                    crdate
                    supplierId
                    supplierBiin
                    supplierBik
                    supplierIik
                    supplierBankNameRu
                    supplierLegalAddress
                    customerId
                    customerBin
                    customerBik
                    customerIik
                    customerBankNameRu
                    customerLegalAddress
                    paymentsTermsRu
                    contractSum
                    contractSumWnds
                    ecEndDate
                    planExecDate
                    faktExecDate
                    contractEndDate
                    refContractTypeId
                    descriptionRu
                    ecCustomerApprove
                    ecSupplierApprove
                    contractMs
                    treasureReqDate
                    treasureNotDate
                    withNds
                    reportStatus
                    enforcement
                }
            }
        """

        query_by_customer = """
            query($customerBin: String!) {
                Contract(filter: { customerBin: $customerBin }, limit: 200){
                    id
                    parentId
                    trdBuyId
                    trdBuyNumberAnno
                    trdBuyNameRu
                    refContractStatusId
                    crdate
                    supplierId
                    supplierBiin
                    supplierBik
                    supplierIik
                    supplierBankNameRu
                    supplierLegalAddress
                    customerId
                    customerBin
                    customerBik
                    customerIik
                    customerBankNameRu
                    customerLegalAddress
                    paymentsTermsRu
                    contractSum
                    contractSumWnds
                    ecEndDate
                    planExecDate
                    faktExecDate
                    contractEndDate
                    refContractTypeId
                    descriptionRu
                    ecCustomerApprove
                    ecSupplierApprove
                    contractMs
                    treasureReqDate
                    treasureNotDate
                    withNds
                    reportStatus
                    enforcement
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

        variables_by_supplier = {"supplierBiin": info}
        variables_by_customer = {"customerBin": info}

        response_by_supplier = make_graphql_request(
            query_by_supplier, variables_by_supplier
        )
        contract_by_supplier = response_by_supplier["data"]["Contract"]
        if contract_by_supplier is not None:
            return contract_by_supplier
        response_by_customer = make_graphql_request(
            query_by_customer, variables_by_customer
        )
        contract_by_customer = response_by_customer["data"]["Contract"]
        if contract_by_customer is not None:
            return contract_by_customer

    def getTradesApp(self, input: str):
        disable_warnings(InsecureRequestWarning)

        info = input

        url = "https://ows.goszakup.gov.kz/v3/graphql"
        headers = {"Authorization": f"Bearer {token}"}

        # Query for searching by bin
        query = """
            query($supplierBinIin: String!) {
                TrdApp(filter: { supplierBinIin: $supplierBinIin }, limit: 200){
                    id
                    supplierId
                    crFio
                    supplierBinIin
                    dateApply
                    AppLots{
                        id
                        statusId
                        price
                        amount
                        Lot{
                            refLotStatusId
                            nameRu
                            descriptionRu
                            customerBin
                            customerNameRu
                            plnPointKatoList
                        }
                    }
                    TrdBuy{
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

        variables = {"supplierBinIin": info}
        response = make_graphql_request(query, variables)
        Trade = response["data"]["TrdApp"]
        return Trade

        # def getRnu(input:str):

        # def getPlans(input:str):
