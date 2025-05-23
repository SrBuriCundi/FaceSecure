import cv2
from model.database import Database
from controller.face_controller import FaceController
from view.camera_view import mostrar_resultados

def main():
    db = Database(host="localhost", user="root", password="", database="face_secure")
    controller = FaceController(db)

    cap = cv2.VideoCapture(0)
    frame_count = 0
    resultados = []  # Guardamos el último resultado para mostrar en los frames intermedios

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Procesar sólo cada N frames
        if frame_count % 5 == 0:
            resultados = controller.procesar_frame(frame)

        # Mostrar el último resultado disponible
        mostrar_resultados(frame, resultados)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    db.cerrar()

if __name__ == "__main__":
    main()
