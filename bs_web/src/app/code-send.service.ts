import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class CodeSendService {

  constructor(private http: HttpClient) {
  }

  private headers = new HttpHeaders({ 'Content-Type': 'application/json', 'Access-Control-Allow-Origin' : '*'});

  sendCode(data: any): Observable<any> {
    return this.http.post<any>("http://localhost:8080/parseprogram", data, { headers: this.headers });
  }

}
