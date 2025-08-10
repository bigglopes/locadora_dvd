import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import os

# Initialize Faker for generating realistic data
fake = Faker('pt_BR')  # Brazilian Portuguese for realistic CPF and names

def generate_cpf():
    """Generate a valid CPF number"""
    def calculate_digit(cpf_digits):
        total = sum(int(digit) * weight for digit, weight in zip(cpf_digits, range(len(cpf_digits) + 1, 1, -1)))
        remainder = total % 11
        return '0' if remainder < 2 else str(11 - remainder)
    
    # Generate first 9 digits
    cpf_digits = [str(random.randint(0, 9)) for _ in range(9)]
    
    # Calculate verification digits
    first_digit = calculate_digit(cpf_digits)
    cpf_digits.append(first_digit)
    
    second_digit = calculate_digit(cpf_digits)
    cpf_digits.append(second_digit)
    
    return ''.join(cpf_digits)

def populate_clients(cursor, num_clients=200):
    """Populate the database with sample clients"""
    print(f"Creating {num_clients} sample clients...")
    
    clients = []
    used_cpfs = set()
    
    for i in range(num_clients):
        # Generate unique CPF
        cpf = generate_cpf()
        while cpf in used_cpfs:
            cpf = generate_cpf()
        used_cpfs.add(cpf)
        
        # Generate client data
        nome = fake.name()
        telefone = fake.phone_number()[:15]  # Limit phone number length
        endereco = fake.address().replace('\n', ', ')[:100]  # Limit address length
        
        clients.append((cpf, nome, telefone, endereco))
    
    # Insert clients into database
    cursor.executemany(
        "INSERT INTO clientes (cpf, nome, telefone, endereco) VALUES (?, ?, ?, ?)",
        clients
    )
    
    print(f"✓ Created {num_clients} clients")
    return [client[0] for client in clients]  # Return CPFs

def populate_dvds(cursor, num_dvds=50):
    """Populate the database with sample DVDs"""
    print(f"Creating {num_dvds} sample DVDs...")
    
    # Sample movie data
    movies = [
        "O Poderoso Chefão", "Pulp Fiction", "O Senhor dos Anéis", "Matrix", "Cidade de Deus",
        "Tropa de Elite", "Central do Brasil", "Carandiru", "Dona Flor e Seus Dois Maridos",
        "O Auto da Compadecida", "Que Horas Ela Volta?", "Aquarius", "Bacurau", "Parasita",
        "Coringa", "Vingadores", "Homem-Aranha", "Batman", "Superman", "Mulher Maravilha",
        "Titanic", "Avatar", "Jurassic Park", "Star Wars", "Indiana Jones", "Rocky",
        "Rambo", "Terminator", "Alien", "Predador", "Die Hard", "Lethal Weapon",
        "Mad Max", "Blade Runner", "Ghostbusters", "Back to the Future", "E.T.",
        "Jaws", "The Shining", "Psycho", "Casablanca", "Gone with the Wind",
        "Citizen Kane", "Vertigo", "Singin' in the Rain", "Some Like It Hot",
        "The Wizard of Oz", "Lawrence of Arabia", "Sunset Boulevard", "On the Waterfront"
    ]
    
    dvds = []
    for i in range(min(num_dvds, len(movies))):
        nome = movies[i]
        sinopse = fake.text(max_nb_chars=200)
        ano_lancamento = random.randint(1970, 2023)
        ano_aquisicao = random.randint(ano_lancamento, 2024)
        disponivel = random.choice([True, False])
        
        dvds.append((nome, sinopse, ano_lancamento, ano_aquisicao, disponivel))
    
    # Insert DVDs into database
    cursor.executemany(
        "INSERT INTO dvds (nome, sinopse, ano_lancamento, ano_aquisicao, disponivel) VALUES (?, ?, ?, ?, ?)",
        dvds
    )
    
    print(f"✓ Created {len(dvds)} DVDs")
    return list(range(1, len(dvds) + 1))  # Return DVD IDs

def populate_rentals(cursor, client_cpfs, dvd_ids, months=2):
    """Populate the database with sample rentals for the last 2 months"""
    print(f"Creating rental data for the last {months} months...")
    
    # Calculate date range for the last 2 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    rentals = []
    rental_count = 0
    
    # Generate rentals
    for _ in range(random.randint(300, 500)):  # Random number of rentals
        cliente_cpf = random.choice(client_cpfs)
        dvd_id = random.choice(dvd_ids)
        
        # Random rental date within the last 2 months
        rental_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        
        # Random return date (some may be None for unreturned DVDs)
        if random.random() < 0.8:  # 80% chance of being returned
            return_date = rental_date + timedelta(days=random.randint(1, 14))
            if return_date > end_date:
                return_date = None
        else:
            return_date = None
        
        # Random rental value between R$ 3.00 and R$ 8.00
        valor_aluguel = round(random.uniform(3.0, 8.0), 2)
        
        rentals.append((
            cliente_cpf,
            dvd_id,
            rental_date.strftime('%Y-%m-%d %H:%M:%S'),
            return_date.strftime('%Y-%m-%d %H:%M:%S') if return_date else None,
            valor_aluguel
        ))
        rental_count += 1
    
    # Insert rentals into database
    cursor.executemany(
        "INSERT INTO alugueis (cliente_cpf, dvd_id, data_aluguel, data_devolucao, valor_aluguel) VALUES (?, ?, ?, ?, ?)",
        rentals
    )
    
    print(f"✓ Created {rental_count} rental records")

def main():
    """Main function to populate the database"""
    db_path = os.path.join('database', 'locadora.db')
    
    if not os.path.exists(db_path):
        print("Database not found. Please run the main application first to create the database.")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("Starting database population...")
        print("=" * 50)
        
        # Clear existing data (optional)
        response = input("Do you want to clear existing data? (y/N): ").lower()
        if response == 'y':
            cursor.execute("DELETE FROM alugueis")
            cursor.execute("DELETE FROM clientes")
            cursor.execute("DELETE FROM dvds")
            print("✓ Cleared existing data")
        
        # Populate tables
        client_cpfs = populate_clients(cursor, 200)
        dvd_ids = populate_dvds(cursor, 50)
        populate_rentals(cursor, client_cpfs, dvd_ids, 2)
        
        # Commit changes
        conn.commit()
        
        print("=" * 50)
        print("✅ Database population completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Clients: 200")
        print(f"   - DVDs: 50")
        print(f"   - Rentals: ~300-500 (last 2 months)")
        
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()