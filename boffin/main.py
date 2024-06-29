import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from boffin.hero.rest import router as hero_router

app = FastAPI()
app.include_router(hero_router)


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)
graphql_app: GraphQLRouter = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
