from fastapi.testclient import TestClient
from unittest.mock import patch, ANY
from app.main import app
from app.schemas.reservationDto import ReservationCreate, ReservationDelete
from app.models.reservationEntity import Reservation as ReservationModel
from datetime import date, time

client = TestClient(app)

mock_reservation_data = {
    "id": "resa-123",
    "salle_id": "salle-123",
    "date": "2025-06-20",
    "heure": "09:00:00",
    "utilisateur": "jdupont",
    "commentaire": "Réunion projet"
}

mock_reservation_create = ReservationCreate(
    salle_id="salle-123",
    date=date(2025, 6, 20),
    heure=time(9, 0),
    utilisateur="jdupont",
    commentaire="Réunion projet"
)

mock_reservation_delete = ReservationDelete(
    salle_id="salle-123"
)

mock_reservation_model = ReservationModel(
    id="resa-123",
    salle_id="salle-123",
    date=date(2025, 6, 20),
    heure=time(9, 0),
    utilisateur="jdupont",
    commentaire="Réunion projet"
)

mock_reservation_list = [
    ReservationModel(
        id="resa-123",
        salle_id="salle-123",
        date=date(2025, 6, 20),
        heure=time(9, 0),
        utilisateur="jdupont",
        commentaire="Réunion projet"
    ),
    ReservationModel(
        id="resa-456",
        salle_id="salle-456",
        date=date(2025, 6, 21),
        heure=time(10, 0),
        utilisateur="mboulanger",
        commentaire=None
    )
]

class TestReservationRouter:
    @patch('app.routers.reservationController.reservationService.list_reservations')
    def test_list_reservations(self, mock_list_reservations):
        mock_list_reservations.return_value = mock_reservation_list
        response = client.get("/reservations/")
        assert response.status_code == 200
        assert len(response.json()) == 2
        mock_list_reservations.assert_called_once()

    @patch('app.routers.reservationController.reservationService.get_reservations_in_time_slot')
    @patch('app.routers.reservationController.reservationService.create_reservation')
    def test_create_reservation_success(self, mock_create_reservation, mock_get_resa_slot):
        mock_get_resa_slot.return_value = []
        mock_create_reservation.return_value = mock_reservation_model
        response = client.post("/reservations/", json={
            "salle_id": "salle-123",
            "date": "2025-06-20",
            "heure": "09:00:00",
            "utilisateur": "jdupont",
            "commentaire": "Réunion projet"
        })
        assert response.status_code == 200
        assert response.json()["salle_id"] == "salle-123"
        assert response.json()["utilisateur"] == "jdupont"
        mock_get_resa_slot.assert_called_once()
        mock_create_reservation.assert_called_once()

    @patch('app.routers.reservationController.reservationService.get_reservations_in_time_slot')
    def test_create_reservation_conflict(self, mock_get_resa_slot):
        mock_get_resa_slot.return_value = [mock_reservation_model]
        response = client.post("/reservations/", json={
            "salle_id": "salle-123",
            "date": "2025-06-20",
            "heure": "09:00:00",
            "utilisateur": "jdupont",
            "commentaire": "Réunion projet"
        })
        assert response.status_code == 400
        assert "créneau horaire" in response.json()["detail"]
        mock_get_resa_slot.assert_called_once()

    @patch('app.routers.reservationController.reservationService.get_reservation_by_id')
    def test_get_reservation_success(self, mock_get_resa):
        mock_get_resa.return_value = mock_reservation_model
        response = client.get("/reservations/resa-123")
        assert response.status_code == 200
        assert response.json()["id"] == "resa-123"
        mock_get_resa.assert_called_once_with(ANY, "resa-123")

    @patch('app.routers.reservationController.reservationService.get_reservation_by_id')
    def test_get_reservation_not_found(self, mock_get_resa):
        mock_get_resa.return_value = None
        response = client.get("/reservations/introuvable")
        assert response.status_code == 404
        assert "non trouvée" in response.json()["detail"]
        mock_get_resa.assert_called_once_with(ANY, "introuvable")

    @patch('app.routers.reservationController.reservationService.get_reservation_by_id')
    @patch('app.routers.reservationController.reservationService.delete_reservation')
    def test_delete_reservation_success(self, mock_delete_reservation, mock_get_resa):
        mock_get_resa.return_value = mock_reservation_model
        mock_delete_reservation.return_value = mock_reservation_model

        response = client.delete("/reservations/resa-123")

        assert response.status_code == 200
        assert response.json()["id"] == "resa-123"
        mock_get_resa.assert_called_once_with(ANY, "resa-123")
        mock_delete_reservation.assert_called_once_with(ANY, "resa-123")

    @patch('app.routers.reservationController.reservationService.get_reservation_by_id')
    def test_delete_reservation_not_found(self, mock_get_resa):
        mock_get_resa.return_value = None

        response = client.delete("/reservations/resa-introuvable")

        assert response.status_code == 404
        assert "non trouvée" in response.json()["detail"]
        mock_get_resa.assert_called_once_with(ANY, "resa-introuvable")
