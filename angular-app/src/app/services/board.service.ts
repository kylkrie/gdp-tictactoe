import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, Observable } from 'rxjs';

interface Board {
  id: number;
  user_id: string;
  spaces: string;
  result: string;
}

interface BoardResponse {
  board: Board
}

@Injectable({
  providedIn: 'root'
})
export class BoardService {
  // these should be environment variables
  private apiUrl = 'http://localhost:4000/api/boards/v1'; 
  // hard coded a token instead of doing any auth
  // I was going to do more with the front end
  // but decided against it
  private token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJuYW1lIjoiVGVzdCBVc2VyIiwiaWF0IjoxNTE2MjM5MDIyfQ.NomeFZ-b1bLL9QOQQkC2dwD0lW03Ehku1IBoSrDEQ6M"

  constructor(private http: HttpClient) {
  }

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.token}`
    });
  }

  createGame(): Observable<Board> {
    return this.http.post<BoardResponse>(this.apiUrl, {}, { headers: this.getHeaders() })
      .pipe(map(response => response.board));
  }

  makeMove(id: number, position: number): Observable<Board> {
    return this.http.post<BoardResponse>(`${this.apiUrl}/${id}/move`, { position },{ headers: this.getHeaders() })
      .pipe(map(response => response.board));
  }
}
