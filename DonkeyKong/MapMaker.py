def makeMap(self):
    for i in range(0, self._height // 15 + 1):
        row = []
        for j in range(0, self._width // 15):
            row.append(0)
        self.map.append(row)


def makeWalls(self):  # Wall = 1
    for i in range(0, (self._height // 15) - 4):
        self.map[i][0] = self.map[i][self._width // 15 - 1] = 1
    for i in range(0, (self._height // (15 * 5))):
        for j in range(0, self._width // 15):
            self.map[i * 5][j] = 1


def makeLadders(self):  # Ladder = 2
    for i in range(1, (self._height // (15 * 5) - 1)):
        ladderPos = math.floor(random.random() * (self._width / 30))
        ladderPos = int(10 + ladderPos)
        for k in range(0, 5):
            self.map[i * 5 + k][ladderPos] = self.map[i * 5 + k][32 - ladderPos] = 2


def makePlayer(self):  # Player = 3
    self.map[34][1] = self.map[33][1] = 3


def drawImages(self):
    self.playerDrawn = 0
    for x in range(len(self.map)):
        for y in range(len(self.map[x])):
            if self.map[x][y] == 1:
                wallLabel = QLabel()
                pix = QPixmap('wood_block.png')
                pixx = pix.scaled(QSize(self.image_size, self.image_size))
                wallLabel.setPixmap(pixx)
                wallLabel.move(y * 15 + 15 / 2, x * 15 + 15 / 2)
                self.hbox.addWidget(wallLabel, x * 15 + 15 / 2, y * 15 + 15 / 2)

            if self.map[x][y] == 2:
                ladderLabel = QLabel()
                pix = QPixmap('ladder.png')
                pixx = pix.scaled(QSize(self.image_size, self.image_size))
                ladderLabel.setPixmap(pixx)
                ladderLabel.move(y * 15 + 15 / 2, x * 15 + 15 / 2)
                self.hbox.addWidget(ladderLabel, x * 15 + 15 / 2, y * 15 + 15 / 2)

            if self.map[x][y] == 3:
                if self.playerDrawn == 0:
                    self.playerDrawn = 1
                else:
                    playerLabel = QLabel()
                    pix = QPixmap('ItsAMeRight.png')
                    pixx = pix.scaled(QSize(self.image_size, self.image_size))
                    playerLabel.setPixmap(pixx)
                    playerLabel.move(y * 15 + 15 / 2, x * 15 + 15 / 2)
                    self.hbox.addWidget(playerLabel, x * 15 + 15 / 2, y * 15 + 15 / 2)


# def clearScreen(self):
# Clear previous screen

def initializeBoard(self):
    # self.clearScreen()
    self.makeMap()
    self.makeWalls()
    self.makeLadders()
    self.makePlayer()
    print(self.map)
    self.drawImages()