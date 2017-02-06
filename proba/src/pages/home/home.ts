import { Component } from '@angular/core';
import { RESTFULService } from '../../app/services/restful.service';
import { NavController } from 'ionic-angular';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  constructor(public navCtrl: NavController, private restService: RESTFULService) {

  }

  ngOnInit(){
    this.getPosts('treino/');
  }

  getPosts(target) {
    this.restService.get(target).subscribe(res => console.log(res));
  }

}
