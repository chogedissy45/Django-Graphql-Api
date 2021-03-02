# DJANGO API

## Installation
1. Clone this repo to your local directory
2. Enable python virtual environment in the source directory
3. Run <code>pip3 install -r requirements.txt</code> to install all the required packages
4. Run <code>python3 manage.py makemigrations</code>
5. Go to graph_api.schema and replace the api_key = "" with your api key
6. Run <code>python3 manage.py migrate</code>
7. Run <code>python3 manage.py migrate --run-syncdb</code>
8. Create a super user for securing the api <code>python3 manage.py createsuperuser</code> and follow the prompts
9. Run <code>python3 manage.py migrate loaddata dummy.json</code>
10. Run <code>python3 manage.py runserver</code> to start the server at https://127.0.01/8000

## Retrieving Data
The program when started runs locally on port 8000. This opens an <a href="https://127.0.01/8000/admin">admin page</a> that'll require a login.
### Creating a simple query
Navigate to https://127.0.01/8000/admin/graphql in your browser to access a graphiql user interface.

<image src="ss/graphql.png">

<h3>Getting all Customers</h3><br>
<pre>
    query getCustomers{
        customers{
            code
            name
            orders{
                item
                amount
            }
        }
    }
</pre>
<h3>Getting all Orders</h3>
<pre>
    query getOrders{
        orders{
            item
            amount
            time
        }
    }
</pre>
<image src="ss/orders.png">

<h3>Creating an Order</h3>
<pre>
mutation createOrder {
    createOrder(input: {item: "Tortillas", amount: 200, time: 2300}) {
    ok
    order {
      item
      amount
      time
    }
  }
}
</pre>

<h3>Creating a Customer<h3>
<pre>
mutation createCustomer {
    createCustomer(input: {code: 714044854, name: "Tom Hanks", orders: [{id: 1}, {id: 2}]}) {
    ok
    customer {
      code
      orders {
        id
        item
        amount
        time
      }
    }
  }
}

</pre>

## Africastalking SMS integration

When the mutation for creating a new customer having a particular order is run, the api automatically takes the code, user's phone numner and sends an order complete message
<image src="ss/11.png"><image src="ss/22.png">
