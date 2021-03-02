import json
import pytest
from graphene_django.utils.testing import graphql_query


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


# Test you query using the client_query fixture
def getCustomers(client_query):
    response = client_query(
        """
        query getCustomers{
            getCustomers {
                code
                name
                order{
                    id
                    item
                    amount
                    time
                }
            }
        }
        """,
        op_name="getCustomers",
    )

    content = json.loads(response.content)
    assert "errors" not in content
