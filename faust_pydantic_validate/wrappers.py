from functools import wraps
from typing import Type, Any

from faust.types.web import ViewHandlerFun, ViewDecorator, View, Request, Response
from pydantic import BaseModel, ValidationError


def takes_pydantic(model: Type[BaseModel], include_schema: bool = True) -> ViewDecorator:
    def _decorate_view(fun: ViewHandlerFun) -> ViewHandlerFun:
        @wraps(fun)
        async def _inner(view: View, request: Request,
                         *args: Any, **kwargs: Any) -> Response:
            try:
                data: dict = await request.json()
                validated_object: model = model.parse_obj(data)
            except ValidationError as e:
                if include_schema:
                    return view.json(
                        value={
                            'errors': e.errors(),
                            'schema': model.schema()
                        },
                        status=422
                    )
                return view.json(
                    value={
                        'errors': e.errors()
                    }
                )
            return await fun(view, request, validated_object, *args, **kwargs)
        return _inner
    return _decorate_view
