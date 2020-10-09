import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { ClusterSelectionComponent } from './cluster-selection/cluster-selection.component';
import { NewComponent } from './new/new.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {HttpClientModule} from '@angular/common/http';
import {CodeSendService} from './code-send.service';
import {Stationinfo} from './object/stationinfo';
import { GroundingComponent } from './grounding/grounding.component';
import { AppRoutingModule } from './app-routing.module';
import { NgZorroAntdModule, NZ_I18N, zh_CN } from 'ng-zorro-antd';
import { FormsModule } from '@angular/forms';
import { registerLocaleData } from '@angular/common';
import zh from '@angular/common/locales/zh';
import {StationInfoAccessService} from './new/station-info-access.service';

registerLocaleData(zh);

@NgModule({
  declarations: [
    AppComponent,
    NewComponent,
    GroundingComponent,
    ClusterSelectionComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    NgZorroAntdModule,
    FormsModule
  ],
  providers: [CodeSendService, Stationinfo, StationInfoAccessService, { provide: NZ_I18N, useValue: zh_CN }],
  bootstrap: [AppComponent]


})
export class AppModule { }
