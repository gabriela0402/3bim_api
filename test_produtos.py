from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_db
from models import ProdutoDB, PetDB

client = TestClient(app)



def test_listar_produtos_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.all.return_value = [
        ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    ]
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/produtos')

    assert resposta.status_code == 200
    assert resposta.json()[0]['nome'] == 'Teclado'

    app.dependency_overrides.clear()


def test_criar_produto_com_mock():
    db_mock = MagicMock()

    def simular_refresh(produto):
        produto.id = 1

    db_mock.refresh.side_effect = simular_refresh
    app.dependency_overrides[get_db] = lambda: db_mock

    novo_produto = {'nome': 'Monitor', 'preco': 799.90, 'quantidade': 5}
    resposta = client.post('/produtos', json=novo_produto)

    assert resposta.status_code == 201
    assert resposta.json()['id'] == 1
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


def test_obter_produto_por_id_sucesso():
    db_mock = MagicMock()
    produto_mock = ProdutoDB(id=1, nome='Mouse', preco=49.90, quantidade=10)
    db_mock.query.return_value.filter.return_value.first.return_value = produto_mock
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/produtos/1')

    assert resposta.status_code == 200
    assert resposta.json()['nome'] == 'Mouse'

    app.dependency_overrides.clear()


def test_atualizar_produto_sucesso():
    db_mock = MagicMock()
    produto_mock = ProdutoDB(id=1, nome='Teclado Membrana', preco=80.00, quantidade=10)
    db_mock.query.return_value.filter.return_value.first.return_value = produto_mock
    app.dependency_overrides[get_db] = lambda: db_mock

    dados_atualizados = {'nome': 'Teclado Mecânico', 'preco': 150.00, 'quantidade': 8}
    resposta = client.put('/produtos/1', json=dados_atualizados)

    assert resposta.status_code == 200
    assert db_mock.commit.called

    app.dependency_overrides.clear()


def test_remover_produto_sucesso():
    db_mock = MagicMock()
    produto_mock = ProdutoDB(id=1, nome='Roteador', preco=150.00, quantidade=2)
    db_mock.query.return_value.filter.return_value.first.return_value = produto_mock
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/produtos/1')

    assert resposta.status_code == 204
    db_mock.delete.assert_called_once_with(produto_mock)
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()






def test_listar_pets_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.all.return_value = [
        PetDB(id=1, nome='Rex', especie='Cão', raca='Labrador', idade=3)
    ]
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/pets')

    assert resposta.status_code == 200
    assert resposta.json()[0]['nome'] == 'Rex'

    app.dependency_overrides.clear()


def test_criar_pet_com_mock():
    db_mock = MagicMock()

    def simular_refresh(pet):
        pet.id = 1

    db_mock.refresh.side_effect = simular_refresh
    app.dependency_overrides[get_db] = lambda: db_mock

    novo_pet = {'nome': 'Mimi', 'especie': 'Gato', 'raca': 'Siamês', 'idade': 2}
    resposta = client.post('/pets', json=novo_pet)

    assert resposta.status_code == 201
    assert resposta.json()['id'] == 1
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


def test_obter_pet_por_id_sucesso():
    db_mock = MagicMock()
    pet_mock = PetDB(id=1, nome='Mel', especie='Cão', raca='Poodle', idade=5)
    db_mock.query.return_value.filter.return_value.first.return_value = pet_mock
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/pets/1')

    assert resposta.status_code == 200
    assert resposta.json()['nome'] == 'Mel'

    app.dependency_overrides.clear()


def test_atualizar_pet_sucesso():
    db_mock = MagicMock()
    pet_mock = PetDB(id=1, nome='Thor', especie='Cão', raca='Bulldog', idade=4)
    db_mock.query.return_value.filter.return_value.first.return_value = pet_mock
    app.dependency_overrides[get_db] = lambda: db_mock

    dados_atualizados = {'nome': 'Thor Supremo', 'especie': 'Cão', 'raca': 'Bulldog', 'idade': 5}
    resposta = client.put('/pets/1', json=dados_atualizados)

    assert resposta.status_code == 200
    assert db_mock.commit.called

    app.dependency_overrides.clear()


def test_remover_pet_sucesso():
    db_mock = MagicMock()
    pet_mock = PetDB(id=1, nome='Bob', especie='Cão', raca='Beagle', idade=2)
    db_mock.query.return_value.filter.return_value.first.return_value = pet_mock
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/pets/1')

    assert resposta.status_code == 204
    db_mock.delete.assert_called_once_with(pet_mock)
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()