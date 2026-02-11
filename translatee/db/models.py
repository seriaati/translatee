from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from translatee.constants import DEFAULT_TARGET_LANG


class UserSettings(Model):
    id = fields.BigIntField(pk=True)
    lang = fields.CharField(max_length=10, default=DEFAULT_TARGET_LANG)
