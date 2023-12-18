import random

data = ""
with open("./csv-2023-12-15-06-53-16-none-1035-iPhone11-463-53.99-66.09-50.21.csv", 'r') as file:
    data = file.read()

def random_uniform_generator(min, max):
    return random.uniform(min, max)

def random_snore_generator():
    rand = random.randint(0,1)
    return 'none' if rand == 1 else 'snore'

def stringify_scalar_single_digit(input):
    if(input < 10):
        return '0'+ str(input)
    return str(input)

init_string = "csv-2023-12-15-06-53-16-none-1035-iPhone11-463-53.99-66.09-50.21.csv"
string_format = "csv-2023-12-15-{}-{}-16-{}-1035-iPhone11-{}-{:.2f}-{:.2f}-{:.2f}-{}.csv"
init_space = init_string.split('-')

initial_hour = int(init_space[4])
initial_time = int(init_space[5])

filenames =[]

for i in range(0,600):
    initial_time += 1
    if(initial_time == 60):
        initial_hour += 1
        initial_time = 0

    snore = random_snore_generator()
    # avg = random_uniform_generator(50,70)
    # maximum = random_uniform_generator(70,85)
    # first_db = random_uniform_generator(50,51)
    avg = random_uniform_generator(0,90)
    maximum = random_uniform_generator(0,90)
    first_db = random_uniform_generator(0,90)


    # 06-52-17.563

    ms = str.format("{:.3f}",(random_uniform_generator(0,1)))
    ms = ms[1:]
    random_ms = str(random.randint(10,59))+ str(ms)
    event_starting_point = stringify_scalar_single_digit(initial_hour)+ "-" + stringify_scalar_single_digit(initial_time) +"-"+ random_ms


    
    snore_count = 0
    if(snore == 'snore'):
        snore_count = random.randint(1,15)
    

    new_file = string_format.format(
        stringify_scalar_single_digit(initial_hour), 
        stringify_scalar_single_digit(initial_time),
        snore,
        snore_count,
        avg,
        maximum,
        first_db,
        event_starting_point
        )

    
    filenames.append(new_file)


for generated_file_name in filenames:
    with open("./csvFolder/" + generated_file_name, 'w') as f:
        f.write(data)
    f.close()


print("Done")
