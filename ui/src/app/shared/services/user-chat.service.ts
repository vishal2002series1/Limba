import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, map } from 'rxjs';
import { apiConfig } from 'src/app/constants/environment';
import { Client, ContentResponse, UserProfile } from 'src/app/constants/model';

@Injectable({
  providedIn: 'root'
})
export class UserChatService {

  private getCurrUser = new BehaviorSubject<string>('');
  currUser = this.getCurrUser.asObservable();

  private readonly USERNAME = apiConfig.username;
  private readonly PASSWORD = apiConfig.password;
  private readonly API_URL = apiConfig.apiURL;
  private readonly BASE_URL = apiConfig.baseURL;
  
  private readonly httpOptions = new HttpHeaders(
    {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(`${this.USERNAME}:${this.PASSWORD}`)
    }
  )

  //   private readonly httpOptions = new HttpHeaders(
  //   {
  //     'Content-Type': 'application/json',
  //     'Authorization': 'Basic VXNlcjpXYW0tUG9j'
  //   }
  // )

  constructor(private http: HttpClient) { }

  //still used for user chat
  getQueryResult(
    // search_mode:string, 
    query: string
    // , recency_factor?:number
    ): Observable<ContentResponse> {
    let body = JSON.stringify({ "question":query});
    let endpoint = 'irah/chat';
    // if (search_mode == 'cognitive') {
    //   endpoint = 'chat/cognitive-search';
    // }
    // let url = `${this.API_URL}/${search_mode}-query-question`;
    let url = `${this.API_URL}/${endpoint}`;
    // console.log(url);
    return this.http.post<ContentResponse>(url, body, { headers: this.httpOptions });
  }


  getQueryResultAll(
    // search_mode:string, 
    query: string, page_type: string
    // , recency_factor?:number
    ): Observable<ContentResponse> {
    let body = JSON.stringify({ "question":query});
    let endpoint = page_type;
    // if (search_mode == 'cognitive') {
    //   endpoint = 'chat/cognitive-search';
    // }
    // let url = `${this.API_URL}/${search_mode}-query-question`;
    let url = `${this.API_URL}/${endpoint}`;
    // console.log(url);
    return this.http.post<ContentResponse>(url, body, { headers: this.httpOptions });
  }

  getQueryResultFinancial(
    // search_mode:string, 
    query: string, page_type: string, client_name: string, client_data: Client
    // , recency_factor?:number
    ): Observable<ContentResponse> {
    let body = JSON.stringify({ "question":query, "client_name":client_name, "client_data":client_data});
    // console.log("body:", body);
    let endpoint = page_type;
    // if (search_mode == 'cognitive') {
    //   endpoint = 'chat/cognitive-search';
    // }
    // let url = `${this.API_URL}/${search_mode}-query-question`;
    let url = `${this.API_URL}/${endpoint}`;
    // console.log(url);
    return this.http.post<ContentResponse>(url, body, { headers: this.httpOptions });
  }
  
  getProfile(): Observable<UserProfile[]> {
    return this.http.get<UserProfile[]>(`${this.BASE_URL}/.auth/me`);
  }

  // getRes(): Observable<ContentResponse> {
  //   return this.http.get<ContentResponse>(`./assets/data/results.json`);
  // }

  getUser(user: string) {
    this.getCurrUser.next(user);
  }

  getDocumentLink(path: string, filename: string): Observable<string> {
    const body = {
      path: path,
      filename: filename
    };
    const url = `${this.API_URL}/irah/files/get_documents`;
  
    return this.http.post(url, body, { headers: this.httpOptions, responseType: 'blob' }).pipe(
      map((blob: Blob) => {
        const blobUrl = URL.createObjectURL(blob);
        return blobUrl;
      })
    );
  }  
}