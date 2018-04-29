import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import 'rxjs/add/operator/map'

@Injectable()
export class PotesProvider {
url;
response;
  constructor(public http: HttpClient) {
    //console.log('Hello PotesProvider Provider');
    this.url = 'http://localhost:5000/potes/api/v1.0/potes';
  }
  //return an observable
  getPotes(){

    this.response = this.http.get(this.url)
    .map(res => res);
    console.log('Response ****', this.response);
    
    return this.response;

  }

}
