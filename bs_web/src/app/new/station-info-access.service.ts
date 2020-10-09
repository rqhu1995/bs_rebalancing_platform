import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';

@Injectable()
export class StationInfoAccessService {

    selectedCluster = -1;

    constructor(private http: HttpClient) {
    }

    _handleError(err: HttpErrorResponse | any) {
        return throwError(err.message || 'Error: Unable to complete request.');
    }

    getStationInfo(): Observable<any> {
        return this.http.get('http://127.0.0.1:5000/station_info').pipe(catchError(this._handleError));
    }

    getCluster(data): Observable<any> {
        return this.http.post('http://127.0.0.1:5000/clustering', data).pipe(catchError(this._handleError));
    }

    setSelectedCluster(selectedCluster) {
        this.selectedCluster = selectedCluster;
    }

    getSelectedCluster() {
        return this.selectedCluster;
    }

    getPriority(data): Observable<any> {
        return this.http.post('http://127.0.0.1:5000/priority', data).pipe(catchError(this._handleError));
    }

}
