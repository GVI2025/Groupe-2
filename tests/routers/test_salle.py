from unittest.mock import ANY, patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.salleEntity import Salle as SalleModel
from app.schemas.salleDto import SalleCreate, SalleUpdate

client = TestClient(app)

mock_salle_data = {
    "id": "salle-123",
    "nom": "Salle Test",
    "capacite": 10,
    "localisation": "Bâtiment X",
    "disponible": True,
}

mock_salle_data2 = {
    "id": "salle-456",
    "nom": "Salle 2",
    "capacite": 20,
    "localisation": "Bâtiment Y",
    "disponible": False,
}

mock_salle_create = SalleCreate(
    nom="Salle Test", capacite=10, localisation="Bâtiment X"
)

mock_salle_update = SalleUpdate(
    nom="Salle Modifiée", capacite=20, localisation="Bâtiment Y"
)

mock_salle_model = SalleModel(
    id="salle-123",
    nom="Salle Test",
    capacite=10,
    localisation="Bâtiment X",
    disponible=True,
)

mock_salle_model2 = SalleModel(
    id="salle-456",
    nom="Salle 2",
    capacite=20,
    localisation="Bâtiment Y",
    disponible=False,
)

mock_salle_list = [mock_salle_model, mock_salle_model2]


class TestSalleRouter:
    @patch("app.routers.salleController.salle_service.list_salles")
    def test_list_salles(self, mock_list_salles):
        mock_list_salles.return_value = mock_salle_list
        response = client.get("/salles/")
        assert response.status_code == 200
        assert len(response.json()) == 2
        mock_list_salles.assert_called_once()

    @patch("app.routers.salleController.salle_service.list_salles")
    def test_list_salles_disponible_true(self, mock_list_salles):
        mock_list_salles.return_value = [mock_salle_model]
        response = client.get("/salles/?disponible=true")
        assert response.status_code == 200
        salles = response.json()
        assert len(salles) == 1
        assert salles[0]["disponible"] is True
        mock_list_salles.assert_called_once_with(
            ANY, skip=0, limit=100, disponible=True
        )

    @patch("app.routers.salleController.salle_service.list_salles")
    def test_list_salles_disponible_false(self, mock_list_salles):
        mock_list_salles.return_value = [mock_salle_model2]
        response = client.get("/salles/?disponible=false")
        assert response.status_code == 200
        salles = response.json()
        assert len(salles) == 1
        assert salles[0]["disponible"] is False
        mock_list_salles.assert_called_once_with(
            ANY, skip=0, limit=100, disponible=False
        )

    @patch("app.routers.salleController.salle_service.create_salle")
    def test_create_salle(self, mock_create_salle):
        mock_create_salle.return_value = mock_salle_model
        response = client.post(
            "/salles/",
            json={"nom": "Salle Test", "capacite": 10, "localisation": "Bâtiment X"},
        )
        assert response.status_code == 200
        assert response.json()["nom"] == mock_salle_data["nom"]
        mock_create_salle.assert_called_once()

    @patch("app.routers.salleController.salle_service.get_salle")
    def test_get_salle_success(self, mock_get_salle):
        mock_get_salle.return_value = mock_salle_model
        response = client.get(f"/salles/{mock_salle_data['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == mock_salle_data["id"]
        mock_get_salle.assert_called_once_with(ANY, mock_salle_data["id"])

    @patch("app.routers.salleController.salle_service.get_salle")
    def test_get_salle_not_found(self, mock_get_salle):
        mock_get_salle.return_value = None
        response = client.get("/salles/introuvable")
        assert response.status_code == 404
        assert "non trouvée" in response.json()["detail"]

    @patch("app.routers.salleController.salle_service.update_salle")
    def test_update_salle_success(self, mock_update_salle):
        updated_salle = mock_salle_model
        updated_salle.nom = "Salle Modifiée"
        updated_salle.capacite = 20
        updated_salle.localisation = "Bâtiment Y"
        mock_update_salle.return_value = updated_salle
        response = client.put(
            f"/salles/{mock_salle_data['id']}",
            json={
                "nom": "Salle Modifiée",
                "capacite": 20,
                "localisation": "Bâtiment Y",
            },
        )
        assert response.status_code == 200
        assert response.json()["nom"] == "Salle Modifiée"
        assert response.json()["capacite"] == 20
        mock_update_salle.assert_called_once()

    @patch("app.routers.salleController.salle_service.update_salle")
    def test_update_salle_not_found(self, mock_update_salle):
        mock_update_salle.return_value = None
        response = client.put(
            "/salles/introuvable",
            json={
                "nom": "Salle Modifiée",
                "capacite": 20,
                "localisation": "Bâtiment Y",
            },
        )
        assert response.status_code == 404
        assert "non trouvée" in response.json()["detail"]

    @patch("app.routers.salleController.salle_service.delete_salle")
    def test_delete_salle_success(self, mock_delete_salle):
        mock_delete_salle.return_value = mock_salle_model
        response = client.delete(f"/salles/{mock_salle_data['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == mock_salle_data["id"]
        mock_delete_salle.assert_called_once_with(ANY, mock_salle_data["id"])

    @patch("app.routers.salleController.salle_service.delete_salle")
    def test_delete_salle_not_found(self, mock_delete_salle):
        mock_delete_salle.return_value = None
        response = client.delete("/salles/introuvable")
        assert response.status_code == 404
        assert "non trouvée" in response.json()["detail"]
