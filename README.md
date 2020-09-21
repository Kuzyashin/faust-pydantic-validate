# Dillinger

faust-pydantic-validate is a small decorator to validate post data.

### Installation

```
pip install faust-pydantic-validate
```

### Usage


```
from pydantic import BaseModel
from faust.types.web import Request, Response
from faust.web import View
from faust_pydantic_validate.wrappers import takes_pydantic

app = faust.App(
    'foo',
    broker='kafka://localhost:9092',
)


class FooBar(BaseModel):
    foobar: int


@app.page('/build/')
class Builder(View):

    @takes_pydantic(FooBar, include_schema=True)
    async def post(self, request: Request, validated_object: BaseModel, **kwargs: Any) -> Response:
        return self.json(value=validated_object.dict())

```
---
##### Request data
```
{
    "foobar": 1
}
```
##### Response data
```
{
    "foobar": 1
}
```
-----
##### Request data
```
{
    "foobar": "foo"
}
```
##### Response data (include_schema=True)
```{
    "errors": [
        {
            "loc": [
                "foobar"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ],
    "schema": {
        "title": "FooBar",
        "type": "object",
        "properties": {
            "foobar": {
                "title": "Foobar",
                "type": "integer"
            }
        },
        "required": [
            "foobar"
        ]
    }
}
```

##### Response data (include_schema=False)
```
{
    "errors": [
        {
            "loc": [
                "foobar"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```
---