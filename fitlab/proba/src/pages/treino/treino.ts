import { Component } from '@angular/core';
import { NavController, NavParams} from 'ionic-angular';

@Component({
  templateUrl: 'treino.html'
})
export class TreinoPage {
    item: any;
    constructor(public navCtrl: NavController, public params:NavParams) {
    }


}
