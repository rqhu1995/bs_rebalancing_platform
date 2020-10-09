import {Component} from '@angular/core';
import {StationInfoAccessService} from '../new/station-info-access.service';

@Component({
    selector: 'app-cluster-selection',
    template: `
        <nz-select nzShowSearch nzAllowClear nzPlaceHolder="选择调度子区..." [(ngModel)]="selectedValue"
                   (ngModelChange)="getSelectedCluster()">
            <nz-option nzLabel="调度子区1" nzValue="0"></nz-option>
            <nz-option nzLabel="调度子区2" nzValue="1"></nz-option>
            <nz-option nzLabel="调度子区3" nzValue="2"></nz-option>
            <nz-option nzLabel="调度子区4" nzValue="3"></nz-option>

        </nz-select>
    `,
    styles: [
            `
            nz-select {
                width: 200px;
            }
        `
    ]
})


export class ClusterSelectionComponent {
    selectedValue = null;

    constructor(private stationInfo: StationInfoAccessService) {
    }

    getSelectedCluster() {
        this.stationInfo.setSelectedCluster(this.selectedValue);
    }
}
