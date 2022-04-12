from chess import Chess

game = Chess()

#bishop test
game.play_move((2,0),(2,2))
game.play_move((5,7),(-4,-4))
game.play_move((4,2), (-2,-2))

#knight test
# game.play_move((1,0), (1,2))
# game.play_move((1,7), (1,-2))
# game.play_move((2,2), (1,2))
# game.play_move((2,5), (1,-2))
# game.play_move((3,4), (-1,2))
# game.play_move((3,3), (-1,-2))