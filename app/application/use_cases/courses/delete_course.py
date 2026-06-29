from dataclasses import dataclass
from uuid import UUID

from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.exceptions import CourseNotFoundError


@dataclass(slots=True)
class DeleteCourseComand:
    course_id: UUID


class DeleteCourseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteCourseComand) -> None:
        async with self.uow:
            course = await self.uow.courses.get_by_id(command.course_id)
            if course is None:
                raise CourseNotFoundError("Course not found.")
            await self.uow.courses.remove(course)
            await self.uow.commit()
