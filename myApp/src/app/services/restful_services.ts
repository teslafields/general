import {Injectable} from '@angular/core';
import {Http, Headers, RequestOptions} from '@angular/http';
import 'rxjs/Rx';

@Injectable()
export class RestService{
  http:any;
  baseUrl: String;

  constructor(http:Http){
      this.http = http;
      this.baseUrl = 'http://localhost:5010';
  }

  getFromBack(){

    var auth = new Headers();
    auth.append('Authorization', 'Basic '+btoa("john:matrix"));
    //auth.append('Content-Type', 'application/json');
    return this.http.get(this.baseUrl+'/temperature', {headers: auth}).map(res => res.json());

    /*{
                                                        method: 'GET',
                                                        data: '',
                                                        url: this.baseUrl+'/temperature',
                                                        headers: {
                                                          'Authorization': 'Basic '+btoa("john:matrix")
                                                          }
                                                      })*/

  }
}
