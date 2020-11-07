import {Component, OnInit} from '@angular/core';
import {StationInfoAccessService} from './station-info-access.service';

@Component({
    selector: 'app-new',
    templateUrl: './new.component.html',
    styleUrls: ['./new.component.css'],
})


export class NewComponent implements OnInit {

    dataSet = [];
    displaySet = [];
    clustered = false;
    toggled = false;
    checkPriority = false;
    selectedCluster = 1;
    informationChecked = false;

    constructor(private stationInfo: StationInfoAccessService) {
    }

    ngOnInit() {
    }

    getCurrentStationInfo() {
        this.toggled = true;
        this.displaySet = [];
        this.stationInfo.getStationInfo().subscribe(res => {
                Object.entries(res).forEach(
                    ([key, value]) => {
                        const tmpObj = {station_id: key};
                        Object.entries(value).forEach(
                            ([k, v]) => {
                                if (k == 'cluster' && v == -1){
                                    tmpObj[k] = '不参与调度';
                                } else {
                                    if (k == 'cluster') {
                                        tmpObj[k] = v + 1;
                                    } else {
                                        tmpObj[k] = v;
                                    }
                                }
                            }
                        );
                        this.displaySet.push(tmpObj);
                        console.log(tmpObj);
                    }
                );
            }
        );
    }

    clustering(clusterMethod: string) {
        this.clustered = true;
        this.displaySet = [];
        this.stationInfo.getStationInfo().subscribe(res => {
                Object.entries(res).forEach(
                    ([key, value]) => {
                        const tmpObj = {station_id: key};
                        Object.entries(value).forEach(
                            ([k, v]) => {
                                if (k == 'cluster' && v == -1){
                                    tmpObj[k] = '不参与调度';
                                } else {
                                    if (k == 'cluster') {
                                        tmpObj[k] = v + 1;
                                    } else {
                                        tmpObj[k] = v;
                                    }
                                }
                            }
                        );
                        this.displaySet.push(tmpObj);
                        console.log(tmpObj);
                    }
                );
            }
        );
    }

    filter_cluster() {
        if (this.displaySet.length < 300) {
            this.displaySet = this.dataSet;
        }
        console.log(this.displaySet.length);
        this.dataSet = this.displaySet;
        //
        console.log(this.stationInfo.getSelectedCluster());
        this.selectedCluster = parseInt(String(this.stationInfo.getSelectedCluster()), 10) + 1;
        this.displaySet = this.displaySet.filter(i => i.cluster == this.selectedCluster);
    }


    getPriority() {
        this.checkPriority = true;
        this.stationInfo.getPriority(this.displaySet).subscribe(res => {
            this.displaySet = res;
        });
    }

    compare(a, b) {
        if (a.priority < b.priority) {
            return 1;
        }
        if (a.priority > b.priority) {
            return -1;
        }
        return 0;
    }

    sortByPriority() {
        this.displaySet.sort(this.compare);
    }
}
