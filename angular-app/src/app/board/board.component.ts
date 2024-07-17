import { Component, OnInit } from '@angular/core';
import { BoardService } from '../services/board.service'

interface Board {
  id: number;
  user_id: string;
  spaces: string;
  result: string;
}

@Component({
  selector: 'app-board',
  standalone: true,
  imports: [],
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.scss']
})
export class BoardComponent implements OnInit {
  board: Board | null = null;
  playerSymbol: string = "";

  constructor(private boardService: BoardService) {}

  ngOnInit() {
    this.newGame();
  }

  newGame() {
    this.boardService.createGame().subscribe(
      (newBoard) => {
        this.board = newBoard;

        // the player's symbol should probably be in the board state
        // or even some higher level game state
        // this works for this project for now though
        let count_x = this.board.spaces.split('x').length
        let count_o = this.board.spaces.split('o').length

        // X goes first, if count is the same, its x turn
        this.playerSymbol = count_x == count_o ? 'x' : 'o'
      }
    );
  }

  makeMove(position: number) {
    if (!this.board) return;

    this.boardService.makeMove(this.board.id, position).subscribe(
      (updatedBoard) => {
        this.board = updatedBoard;
      }
    );
  }

  get gameResult(): string {
    if (this.board?.result == 'win_x')
      return "X Wins!"
    else if (this.board?.result == 'win_o')
      return "O Wins!"
    else if (this.board?.result == 'tie')
      return "Tie!"

    return '';
  }
}
