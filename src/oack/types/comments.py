"""Comment types."""

from __future__ import annotations

from pydantic import BaseModel


class Comment(BaseModel):
    id: str
    monitor_id: str = ""
    author_id: str = ""
    author_name: str = ""
    author_avatar: str = ""
    body: str = ""
    parent_id: str | None = None
    anchor_from: str = ""
    anchor_to: str = ""
    is_resolved: bool = False
    resolved_by: str | None = None
    resolved_at: str | None = None
    edited_at: str | None = None
    is_deleted: bool = False
    reply_count: int = 0
    created_at: str = ""


class CommentReply(BaseModel):
    id: str
    comment_id: str
    author_id: str
    author_name: str
    author_avatar: str = ""
    body: str
    created_at: str


class CreateCommentParams(BaseModel):
    body: str
    anchor_at: str | None = None
    anchor_from: str | None = None
    anchor_to: str | None = None


class CommentEdit(BaseModel):
    id: str
    comment_id: str
    body: str
    edited_at: str
