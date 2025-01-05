people = {
  'Harry': {'name': 'Harry', 'mother': {'Lily',"aa","bb"}, 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

for person in people:
    print(person)
    print(people[person]["mother"])
people_name = list(people.keys())
default_value = {"genes": 0, "trait": False}
arg_info = {person: default_value.copy() for person in people_name}
one_gene = {"Harry"} 
two_genes = {"James"} 
have_trait = {"Harry", "James"}

for one in one_gene:
    arg_info[one]["genes"] = 1
for two in two_genes:
    arg_info[two]["genes"] = 2
for have in have_trait:
    arg_info[have]["trait"] = True

print(list(people["Harry"]["mother"]))