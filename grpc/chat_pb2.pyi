from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoolPayload(_message.Message):
    __slots__ = ["boolVal"]
    BOOLVAL_FIELD_NUMBER: _ClassVar[int]
    boolVal: bool
    def __init__(self, boolVal: bool = ...) -> None: ...

class Payload(_message.Message):
    __slots__ = ["msg"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class SendRequest(_message.Message):
    __slots__ = ["recipient", "sender", "sentMsg"]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    SENTMSG_FIELD_NUMBER: _ClassVar[int]
    recipient: Username
    sender: Username
    sentMsg: Payload
    def __init__(self, sender: _Optional[_Union[Username, _Mapping]] = ..., recipient: _Optional[_Union[Username, _Mapping]] = ..., sentMsg: _Optional[_Union[Payload, _Mapping]] = ...) -> None: ...

class Unreads(_message.Message):
    __slots__ = ["errorFlag", "unreads"]
    ERRORFLAG_FIELD_NUMBER: _ClassVar[int]
    UNREADS_FIELD_NUMBER: _ClassVar[int]
    errorFlag: bool
    unreads: str
    def __init__(self, errorFlag: bool = ..., unreads: _Optional[str] = ...) -> None: ...

class Username(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
