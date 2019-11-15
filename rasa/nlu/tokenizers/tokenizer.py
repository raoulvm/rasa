import logging

from typing import Text, List, Optional, Dict, Any

from rasa.nlu.components import Component
from rasa.nlu.constants import (
    MESSAGE_RESPONSE_ATTRIBUTE,
    MESSAGE_TEXT_ATTRIBUTE,
    CLS_TOKEN,
)

logger = logging.getLogger(__name__)


class Token(object):
    def __init__(
        self,
        text: Text,
        offset: int,
        data: Optional[Dict[Text, Any]] = None,
        lemma: Optional[Text] = None,
        end: int = None,
    ):
        self.offset = offset
        self.text = text
        self.end = end if end else offset + len(text)
        self.data = data if data else {}
        self.lemma = lemma or text

    def set(self, prop: Text, info: Any):
        self.data[prop] = info

    def get(self, prop: Text, default: Optional[Any] = None):
        return self.data.get(prop, default)

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (self.offset, self.end, self.text, self.lemma) == (
            other.offset,
            other.end,
            other.text,
            other.lemma,
        )

    def __lt__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (self.offset, self.end, self.text, self.lemma) < (
            other.offset,
            other.end,
            other.text,
            other.lemma,
        )


class Tokenizer(Component):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super(Tokenizer, self).__init__(component_config)

        try:
            self.use_cls_token = self.component_config["use_cls_token"]
        except KeyError:
            raise KeyError(
                "No default value for 'use_cls_token' was set. Please, "
                "add it to the default dict of the tokenizer."
            )

    def add_cls_token(
        self, tokens: List[Token], attribute: Text = MESSAGE_TEXT_ATTRIBUTE
    ) -> List[Token]:
        if (
            attribute in [MESSAGE_RESPONSE_ATTRIBUTE, MESSAGE_TEXT_ATTRIBUTE]
            and self.use_cls_token
            and tokens
        ):
            # +1 to have a space between the last token and the __cls__ token
            idx = tokens[-1].offset + len(tokens[-1].text) + 1
            tokens.append(Token(CLS_TOKEN, idx))

        return tokens
