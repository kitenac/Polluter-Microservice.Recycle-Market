import random
from datetime import timedelta

from factory import LazyFunction
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker # for mocks data

from app.data.orm import Models
from app.data.schemas import *



def time_m(x: int):
    '''time in minutes'''
    return timedelta(minutes=x)

# data predefined by task
WASTE_CATEGORIES = {
    'category': ['биоотходы', 'стекло', 'пластик'],
    'time_to_recycle': [time_m(x) for x in (1, 3, 4)] } 


class ImpossibleToGenerateMock(Exception):
    '''Exception for situation when mock-generation isn`t posible due some constraints'''
    def __init__(self, message, solution):
        super().__init__(message)  
        self.solution = solution  # some compromise to bypass exception - advised from exception creator


# ==== helper functions for mocks - mb move `em in separate file later ====
def get_random_coord(digets: int = 6):
    '''get random float with given number of digets after comma '''
    random_float = random.uniform(0, 1)        # random float
    truncated = float(f"{random_float:.{digets}f}")   # truncating
    return random.randint(0,999999) + truncated



# Create Factory Classes:  This allows you to easily generate instances of your models with realistic data 
faker = Faker() # faker object to generate truth-like data on different topics automatically

# ==== Tables without FK - "low-lvl" tables ====

# LazyFunction - helps create UNIQ values by delaing evaluation of code inside until initing an object | without it poles would get random value, but it`d be same for all instances - due it has been  already counted
class PolluterFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Models.Polluter_OO
    name  = LazyFunction(lambda: f'OO {faker.company()}')   
    x_geo = LazyFunction(get_random_coord)
    y_geo = LazyFunction(get_random_coord)




def WasteCategoryPseudoFactory():
    '''
    all possible wastecategories
        - "Pseudo": due it`s not factoryboy`s Factory - just function that unpacks data predefined by task
    '''
    return [
        Models.WasteCategory(
                category=WASTE_CATEGORIES['category'][i], 
                time_to_recycle=WASTE_CATEGORIES['time_to_recycle'][i]) 
        for i in range(3)
    ]


def PolluterWastePseudoFactory(size, polluters, waste_categories):
    '''
    Generate random Waste by random Polluter in cycle - size times
        - "Pseudo": due it`s not factoryboy`s Factory - polluter_id (FK) can`t be known without calling db (db call is bad for mocks) - so passing it as a "parametr from outside"
    '''
    
    polluter_wastes = []

    # Actual Factory: producing size-count random entities
    for _ in range(size):
        amount = random.randint(1,5)
        # FKs - using relations through indexes, bc ids are auto-generated and not known yet - will be substituted by idx
        polluter_idx = random.randint(0, len(polluters)-1)
        category_idx = random.randint(0, len(waste_categories)-1)

        waste = Models.PolluterWaste(
                amount      = amount,
                polluter_id = polluters[polluter_idx].id,
                category    = waste_categories[category_idx].category
        )
        polluter_wastes.append(waste)

    return polluter_wastes 


# =========================================================== 
# а ещё моки (..._Factory функции) можно в теcтах использовать: - мб пригодится
