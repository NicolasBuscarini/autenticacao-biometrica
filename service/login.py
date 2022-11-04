from PyQt5 import QtGui, uic, QtWidgets
import cv2
import numpy as np
import sqlite3
import time
import fingerprint_enhancer
from matplotlib import pyplot as plt


class Login:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.loginUi3 = uic.loadUi('ui/loginUi3.ui')
        self.home = uic.loadUi('ui/home.ui')
        self.biometria = uic.loadUi('ui/biometria.ui')
        self.loginUi3.btn_acessar.clicked.connect(self.chama_tela_home)
        self.home.pushButton.clicked.connect(self.logout)
        self.loginUi3.show()
        self.app.exec()

    def chama_tela_home(self):
        global db
        user = self.loginUi3.lineEdit_user.text()
        password = self.loginUi3.lineEdit_password.text()
        try:
            db = sqlite3.connect("db/Cadastros_Agentes.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Cadastro_Agentes c WHERE c.usuario = '{}';".format(user));

            user = cursor.fetchall()

            if user == "" and password == "":
                self.loginUi3.loginInvalido.setText("Campos Vazios")
            elif user[0][3] == password:
                self.loginUi3.close()
                self.tipo_de_acesso(user[0][5], user[0][1], user[0][4])
            else:
                self.loginUi3.loginInvalido.setText("Dados de Login ou Senha Incorretos")
        except Exception as e:
            print(e)
            self.loginUi3.loginInvalido.setText("Dados de Login ou Senha Incorretos")
        finally:
            db.close()

    def tipo_de_acesso(self, acesso, nome, biometria_blob):
        self.autenticar(biometria_blob)

        self.home.lineEdit.setText(nome)
        if acesso == 1:
            self.home.lineEdit_2.setText('1')
            self.home.label_4.setText(
                'Informações do nível 1 - Produção agrícola\n Nome da unidade produtora (produtor agrícola) '
                '– Bom Futuro\n Endereço do produtor agrícola - Av. dos Florais, S/N - Ribeirão do Lipa, '
                'Cuiabá - MT\n Produto(s) agrícolas produzidos – Soja, milho e algodão\n Produção anual em '
                'quilogramas – Aproximadamente 1,7 milhão de toneladas\n Destino da produção (mercado '
                'interno ou exportação)\n Número de empregados da unidade produtora - 5 mil\n Quantidade de '
                'máquinas e implementos agrícolas – Em torno de 400 máquinas, sendo elas tanto para '
                'colheita,\nquanto caminhões de transporte\n Nível de automação da unidade produtora – Alto '
                'nível, sendo a maior produtora agrícola do Brasil')
        elif acesso == 2:
            self.home.lineEdit_2.setText('2')
            self.home.label_4.setText(
                'Incentivos fiscais recebidos – Anistia, antecipação de receitas, refinanciamento '
                'tributário, entre outros.\n Impostos municipais pagos – IPTU (Imposto Predial '
                'Territorial '
                'Urbano)\n*poderá incidir caso trata-se de propriedade localizada em zona urbana ou '
                'urbanizada*;\n ISSQN (Imposto Sobre Serviços de Qualquer Natureza).\n Impostos estaduais '
                'recolhidos – ICMS (Imposto sobre Circulação de Mercadorias);\n IPVA (Imposto sobre '
                'Propriedade de Veículos Automotores).\n Impostos federais pagos – IRPJ (Imposto de '
                'Renda);\n IE (Imposto de Exportação);\n ITR (Imposto Territorial Rural)\n *poderá '
                'incidir '
                'caso trata-se de propriedade localizada em zona rural*; Cofins, PIS PASEP, CSLL, '
                'INSS.\n Taxas federais pagas – Taxa de licenciamento ambiental para instalação e '
                'operação '
                'da empresa.')
        elif acesso == 3:
            self.home.lineEdit_2.setText('3')
            self.home.label_4.setText('Usuario autentificado biometricamente.')

    def autenticar(self, biometria_blob):
        self.biometria.show()
        self.biometria.progressBar.setRange(0, 100)
        self.biometria.progressBar.setValue(0)
        self.biometria.label.setPixmap(QtGui.QPixmap(''))
        self.biometria.image.setPixmap(QtGui.QPixmap(''))
        self.write_blob_file(biometria_blob)

        def progress():
            counter = 0
            self.biometria.image.setPixmap(QtGui.QPixmap('assets/images/fingerprint.png'))
            self.biometria.text_progressbar.setText('Recebendo imagem por arquivo')

            while int(counter) <= 100:
                min_match_count = 10
                if counter == 25:
                    self.biometria.text_progressbar.setText('Aplicando Binarização')
                    img1 = cv2.imread("assets/images/fingerprint.png", 0)
                    img2 = cv2.imread('assets/images/temp.png')
                    img1 = fingerprint_enhancer.enhance_Fingerprint(img1)
                    img2 = fingerprint_enhancer.enhance_Fingerprint(img2)
                    cv2.imwrite("assets/results/img_binarizada.png", img1)
                    self.biometria.image.setPixmap(QtGui.QPixmap('assets/results/img_binarizada.png'))

                if counter == 50:
                    self.biometria.text_progressbar.setText('Extração de Características')
                    # Iniciando SIFT
                    sift = cv2.SIFT_create()
                    # Encontrando Keypoints e descriptors com SIFT
                    kp1, des1 = sift.detectAndCompute(img1, None)
                    kp2, des2 = sift.detectAndCompute(img2, None)
                    kp_img = cv2.drawKeypoints(img1, kp1, None, color=(0, 255, 0),
                                               flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    cv2.imwrite("assets/results/keypoints.png", kp_img)
                    self.biometria.image.setPixmap(QtGui.QPixmap('assets/results/keypoints.png'))
                    time.sleep(0.1)

                if counter == 75:
                    self.biometria.image.setPixmap(QtGui.QPixmap(''))
                    flann_index_kdtree = 1
                    index_params = dict(algorithm=flann_index_kdtree, trees=10)
                    search_params = dict(checks=50)
                    flann = cv2.FlannBasedMatcher(index_params, search_params)
                    matches = flann.knnMatch(des1, des2, k=2)
                    # Agrupando todos os matches
                    good = []
                    for m, n in matches:
                        if m.distance < 0.7 * n.distance:
                            good.append(m)
                    # Verificando os matches e entregando resultado
                    if len(good) > min_match_count:
                        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                        m, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                        matches_mask = mask.ravel().tolist()
                        h, w = img1.shape
                        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                        dst = cv2.perspectiveTransform(pts, m)
                        img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
                        print("Obteve matches o suficiente - {}/{}".format(len(good), min_match_count))
                        self.biometria.text_progressbar.setText(
                            "Obteve matches o suficiente - {}/{}".format(len(good), min_match_count))
                    else:
                        print("Não obteve matches o suficiente - {}/{}".format(len(good), min_match_count))
                        self.biometria.text_progressbar.setText(
                            "Não obteve matches o suficiente - {}/{}".format(len(good), min_match_count))
                        matches_mask = None
                        return False
                    draw_params = dict(matchColor=(0, 255, 0),
                                       singlePointColor=None,
                                       matchesMask=matches_mask,
                                       flags=2)
                    img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
                    plt.imshow(img3, )
                    plt.savefig('assets/results/Matches.png', format='png')
                    self.biometria.label.setPixmap(QtGui.QPixmap('assets/results/Matches.png'))
                    time.sleep(0.1)

                counter += 1
                self.biometria.progressBar.setValue(int(counter))
                time.sleep(0.2)

                if counter == 100:
                    self.biometria.text_progressbar.setText('Biometria Validada')
                    self.biometria.image.setPixmap(QtGui.QPixmap('assets/results/Matches.png'))
                    time.sleep(5)
                    self.biometria.close()
                    self.home.show()
                    return True

        def progress_error():
            time.sleep(7)
            return self.logout()

        self.biometria.pushButton.clicked.connect(lambda: progress() if progress() else progress_error())

    @staticmethod
    def write_blob_file(blob):
        imagem = open("assets/images/temp.png", "wb")
        imagem.write(blob)
        imagem.close()

    def logout(self):
        self.home.close()
        self.loginUi3.show()
        self.loginUi3.lineEdit_user.setText("")
        self.loginUi3.lineEdit_password.setText("")
        self.loginUi3.loginInvalido.setText("")
