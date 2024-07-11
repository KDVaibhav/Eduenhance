from een.db.articles import ArticlesRepository
def articles(school):
    return ArticlesRepository(school)

from een.db.comments import CommentsRepository
def comments(school):
    return CommentsRepository(school)

from een.db.proposals import ProposalsRepository
def proposals(school):
    return ProposalsRepository(school)

from een.db.sessions import SessionsRepository
def sessions(school):
    return SessionsRepository(school)

from een.db.users import UsersRepository
def users(school):
    return UsersRepository(school)

from een.db.votes import VotesRepository
def votes(school):
    return VotesRepository(school)

from een.db.roles import RolesRepository
def roles(school):
    return RolesRepository(school)

from een.db.laws import LawsRepository
def laws(school):
    return LawsRepository(school)

from een.db.school import SchoolRepository
def school():
    return SchoolRepository()

from een.db.timetable import TimetableRepository
def timetable(school):
    return TimetableRepository(school)

from een.db.attendance import AttendanceRepository
def attendance(school):
    return AttendanceRepository(school)

from een.db.exams import ExamsRepository
def exams(school):
    return ExamsRepository(school)

from een.db.marks import MarksRepository
def marks(school):
    return MarksRepository(school)

from een.db.lessonplans import LessonplansRepository
def lessonplans(school):
    return LessonplansRepository(school)

from een.db.lastids import LastidsRepository
def lastids(school):
    return LastidsRepository(school)

from een.db.classes import ClassesRepository
def classes(school):
    return ClassesRepository(school)

from een.db.subjects import SubjectsRepository
def subjects(school):
    return SubjectsRepository(school)

from een.db.transactions import TransactionsRepository
def transactions(school):
    return TransactionsRepository(school)

from een.db.balances import BalancesRepository
def balances(school):
    return BalancesRepository(school)

from een.db.periods import PeriodsRepository
def periods(school):
    return PeriodsRepository(school)

from een.db.leave import LeaveRepository
def leave(school):
    return LeaveRepository(school)

from een.db.payment import PaymentRepository
def payment(school):
    return PaymentRepository(school)

from een.db.news import NewsRepository
def news(school):
    return NewsRepository(school)