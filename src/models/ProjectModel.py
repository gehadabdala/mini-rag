# هنا هحتاج من ال db_schema ال project اللي هتعامل معاه
from models.BaseDataModel import BaseDataModel
from .db_schemas.project import Project
from .enums.DatabaseEnum import DatabaseEnum


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        # اقدر امسك التابل اللي معايا كده
        self.collection = self.db_client[DatabaseEnum.COLLECTION_PROJECT_NAME.value]

    # عندي function async وبنادي عليها جوا ال init ببساطه
    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)  # كده هنا نده علي ال init
        await instance.init_collection()  # هنا نده علي ال init_collection عشان يتاكد ان ال collection موجوده في ال db ولو مش موجوده هتتعمل
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DatabaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"], name=index["name"], unique=index["unique"]
                )

    async def create_project(self, project: Project):
        # هنا هضيف المشروع بتاعي للقاعدة, وكل ما هنادي ال motor هستخدم await
        result = await self.collection.insert_one(
            project.dict(by_alias=True, exclude_unset=True)
        )  # dict(by_alias=True) => عشان ال alias اللي عملناه في ال project model يشتغل
        project_id = result.inserted_id
        return project_id

    async def get_project_or_create_one(self, project_id: str):
        # انا بدور عندك علي ال project_id اللي انت عايزه, ولو مش لاقيه هعمل واحد جديد
        record = await self.collection.find_one({"project_id": project_id})
        if record is None:
            # create new project
            project = Project(project_id=project_id)  # create object
            project = await self.create_project(project=project)  # save to db
            return project

        return Project(
            **record
        )  # بيحول ال dic كأني اديت كل كل value فال dic عشان نكون الموديل

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        # هنا هجيب كل المشاريع اللي عندي في القاعدة, وهعمل pagination عشان ما اجيبش كلهم مرة واحدة
        # count total number of documents
        total_documents = await self.collection.count_documents({})

        # calculate total pages
        total_pages = total_documents // page_size
        if total_documents % page_size != 0:
            total_pages += 1

        # calculate skip
        # self.collection.find().skip((page - 1) *page_size).limit(page_size)

        # فيه حاجه اسمها cursor بيخليك كأنك مؤشر وتقعد تلف عليه عشان تجيب كل ال data اللي عندك في ال collection

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for document in cursor:  # async because motor
            projects.append(Project(**document))

        return projects, total_pages
