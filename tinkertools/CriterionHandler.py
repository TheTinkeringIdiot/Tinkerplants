from tinkertools.utils import *

class CriterionHandler:
    criterions = []

    def __init__(self, criterions):
        self.criterions = criterions

    def parse_criteria(self):
        criteria = []
        
        for criterion in self.criterions:
            operator = criterion.operator

            try:
                if operator == 42: 
                    if len(criteria) <= 0: continue
                    operand = criteria.pop()
                    operand.append('Not')
                    criteria.append(operand)
                
                elif operator == 4:
                    if len(criteria) <= 0: continue
                    oper1 = criteria.pop()
                    oper2 = criteria.pop()
                    oper2.append('And')
                    criteria.extend([oper2, oper1])

                elif operator == 3:
                    if len(criteria) <= 0: continue
                    oper1 = criteria.pop()
                    oper2 = criteria.pop()
                    oper2.append('Or')
                    criteria.extend([oper2, oper1])

                else:
                    result = self.interpret_criterion(criterion)
                    criteria.append(result)

            except:
                continue

        return criteria

    def interpret_criterion(self, criterion):

        if criterion.operator in USE_ON_OPERATOR.keys():
            crit = [USE_ON_OPERATOR[criterion.operator]]
            return crit

        elif criterion.operator in [22, 107]: # StatBitSet/StatBitNotSet
            crit = []
            val1 = STAT[criterion.value1]
            crit.append(val1)

            if criterion.operator == 22:
                crit.append('Is')
            else:
                crit.append('IsNot')

            # breakpoint()
            if val1 == 'Expansion':
                crit.append(str(EXPANSION_FLAG(criterion.value2)).replace('EXPANSION_FLAG.', ''))
            elif val1 == 'Specialization':
                crit.append(str(SPECIALIZATION_FLAG(criterion.value2)).replace('SPECIALIZATION_FLAG.', ''))
            elif val1 == 'WornItem':
                crit.append(str(WORN_ITEM(criterion.value2)).replace('WORN_ITEM.', ''))
            elif val1 == 'SelectedTargetType':
                crit.append('Monster')
            else:
                crit.append(str(WEAPON_TYPE(criterion.value2)).replace('WEAPON_TYPE.', ''))
            return crit

        elif criterion.operator in [0, 1, 2, 24, 42]:  # StatValue
            crit = []
            val1 = STAT[criterion.value1]
            crit.append(val1)

            if val1 == 'Profession' or val1 == 'VisualProfession':
                val2 = PROFESSION[criterion.value2]
            elif val1 == 'Faction':
                val2 = FACTION[criterion.value2]
            elif val1 == 'Gender':
                val2 = GENDER[criterion.value2]
            else:
                val2 = criterion.value2
            
            compare = OPERATOR[criterion.operator]
            if compare == 'StatEqual':
                crit.append('==')
                crit.append(val2)
            if compare == 'StatGreaterThan':
                crit.append('>=')
                crit.append(val2 + 1)
            elif compare == 'StatLessThan':
                crit.append('<=')
                crit.append(val2 - 1)
            elif compare == 'StatNotEqual':
                crit.append('!=')
                crit.append(val2)
            return crit

        elif criterion.operator in [31, 32, 33, 34, 35, 36, 91, 108, 109, 127]: # Item in val2
            crit = [OPERATOR[criterion.operator]]
            itemID = criterion.value2
            targetItem = Item.objects.get(aoid=itemID)
            crit.append(f'<a href="/item/{itemID}">{targetItem.name}</a>')
            return crit

        elif criterion.operator in [93, 94, 97]: # PerkTrained/PerkLocked/PerkNotLocked
            crit = [OPERATOR[criterion.operator]]
            crit.append(criterion.value2)
            return crit

        elif criterion.operator in [98, 99]: # True/False
            crit = [OPERATOR[criterion.operator]]
            return crit

        elif criterion.operator in [44, 45, 66, 70, 80, 83, 85, 86, 89, 103, 104, 111, 112, 114, 115, 116, 118, 119, 120, 121, 122, 123, 124, 125, 129, 130, 131, 132, 133, 134, 135, 136]:
            crit = [STAT[criterion.value1]]
            crit.append(OPERATOR[criterion.operator])
            crit.append(criterion.value2)
            return crit

        elif criterion.operator in [91, 92, 101, 102, 106, 117, 138]: # operator then value2
            crit = [OPERATOR[criterion.operator]]
            crit.append(criterion.value2)
            return crit

        elif criterion.operator in [88]: # Use location
            crit = [OPERATOR[criterion.operator]]
            crit.append(str(ARMOR_SLOT(criterion.value2)).replace('ARMOR_SLOT.', ''))
            return crit
        
        elif criterion.operator in [50]:
            crit = [TARGET[criterion.value1]]
            crit.append(OPERATOR[criterion.operator])
            crit.append(TARGET[criterion.value2])
            return crit

        else: 
            breakpoint()


# def flatten(lst):
#     result = []
#     for i in lst:
#         if isinstance(i, list):
#             result.extend(flatten(i))
#         else:
#             result.append(i)
#     return result

# def parse(criteria, invert=False):
#     # breakpoint()
#     if isinstance(criteria, list):
#         if len(criteria) == 3:
#             operator = criteria[1]
#             if operator == 'And':
#                 return f"({parse(criteria[0])} AND {parse(criteria[2])})"
#             elif operator == 'Or':
#                 return f"({parse(criteria[0])} OR {parse(criteria[2])})"
#             elif operator == 'Not':
#                 return f"NOT ({parse(criteria[2])})"
#         else:  # Assume non-operator
#             return str(criteria)
#     else:  # Assume non-operator
#         return str(criteria)
    
# def print_tree(criteria, indent=0):
#     # breakpoint()
#     if isinstance(criteria, list):
#         if len(criteria) == 3:
#             operator = criteria[1]
#             if not operator in ['And', 'Or', 'Not']:
#                 print('  ' * indent + str(criteria))
#             # elif operator == 'Or':
#             #     print('  ' * indent + operator)
#             #     print_tree(criteria[0], indent + 1)
#             #     print_tree(criteria[2], indent + 1)
#             else:
#                 print('  ' * indent + operator)
#                 print_tree(criteria[0], indent + 1)
#                 print_tree(criteria[2], indent + 1)
#         else:  # Assume non-operator
#             print('  ' * indent + str(criteria))
#     else:  # Assume non-operator
#         print('  ' * indent + str(criteria))