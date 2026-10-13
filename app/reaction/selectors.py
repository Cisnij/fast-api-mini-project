import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.reaction.models import Reaction
from app.users.models import User


async def get_post_reaction_selectors(post_id:uuid.UUID,db:AsyncSession,user:User):
    result = await db.execute(
        select(Reaction)
        .where(Reaction.post_id==post_id)
        .where(Reaction.user_id==user.id)
    )
    reaction = result.scalars().first()
    if not reaction:
        return None
    return reaction

async def get_reactions_post_selectors(post_id:uuid.UUID, db:AsyncSession):
    reactions = await db.execute(
        select(Reaction)
        .options(joinedload(Reaction.user))
        .where(Reaction.post_id == post_id)
    )
    reactions = reactions.scalars().all()
    return {
        "total": len(reactions),
        "users": [reaction.user for reaction in reactions]
    }