from api import *

schema = Schema(query=Query)
app    = Flask(__name__)
app.debug = True
app.add_url_rule("/graphql",
                 view_func = GraphQLView.as_view("graphql",
                                                  schema   = schema,
                                                  graphiql = True))


if __name__ == '__main__':
    app.run()
