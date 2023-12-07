from typing import Optional

from fastapi import APIRouter, Response, Header, HTTPException, Query
from starlette.responses import JSONResponse

from common.auth import get_user_or_raise_401
from data.company import RegisterDataCompany, CompanyInfoForEdit, JobAds, Status, JobAdsReturn
from data.professional_model import StatusForPro
from data.skill_model import CreateSkill, SkillLevel
from routers.helpers import username_exists, exists
from services import companies_service, login_service, professionals_service
from services.companies_service import create_skill_com
from services.professionals_service import create_skill_pro
from services.skill_service import create_skill, insert_into

skill_router = APIRouter(prefix='/Skill', tags=['Skill'])


@skill_router.post('/ads')
def create_skills(skill: CreateSkill, company_ads: Optional[int] = None, data: SkillLevel = Query(description="Choose your skill level"),
                  x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if company_ads is not None and user.type == 1:
        raise HTTPException(status_code=401,
                            detail='Only professional can use company ads')

    if company_ads is None and user.type == 0:
        raise HTTPException(status_code=401,
                            detail="you can't use empty company ads")

    if user.type == 1:
        companies_id = companies_service.find_company_id_by_username_id(user.id)
        if exists(companies_id, table_name='job_ads'):
            skill_com = create_skill(skill.skill, data.value)
            insert_into(companies_id, skill_com.id, user.type)

        raise HTTPException(status_code=401,
                            detail='First you should make Job Ads')

    else:
        user.type = 0
        if exists(company_ads, table_name='company_ads'):
            skill_pro = create_skill(skill.skill, data.value)
            insert_into(company_ads, skill_pro.id, user.type)
            return JSONResponse(status_code=200, content=f'You successful added {skill_pro.skill}')
        raise HTTPException(status_code=401,
                         detail='First you should make Company Ads')


