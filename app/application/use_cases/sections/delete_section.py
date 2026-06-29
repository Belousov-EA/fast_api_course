from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import SectionNotFoundError, ModuleNotFoundError

from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteSectionCommand:
    section_id: UUID


class DeleteSectionUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteSectionCommand) -> None:
        async with self.uow:
            section = await self.uow.sections.get_by_id(command.section_id)
            if section is None:
                raise SectionNotFoundError("Section not found.")
            module = await self.uow.sections.get_by_id(section.get_module_id())
            if module is None:
                raise ModuleNotFoundError("Error not found.")
            module.remove_section(command.section_id)
            await self.uow.module.update(module)
            await self.uow.section.remove(section)
            await self.uow.commit()
