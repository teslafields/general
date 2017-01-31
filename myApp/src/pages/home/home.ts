import { Component } from '@angular/core';
import { RestService } from '../../app/services/restful_services';
import { NavController } from 'ionic-angular';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
  item: any;
  constructor(public navCtrl: NavController, private restful:RestService) {

  }

  ngOnInit(){
    this.getTemp();
  }

  getTemp(){
    this.restful.getFromBack().subscribe(response => {this.item = response.result.temperature[1]; console.log(this.item)});

  }


}
