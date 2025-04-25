import React from 'react';
import { Spinner } from 'reactstrap';

//It shows spinner
export const Loading = () => {
    return(
        <div className="col-12">
            {/*<span className="fa fa-spinner fa-pulse fa-3x fa-fw text-primary"></span>*/}
            <Spinner color="dark" />
            <p>Loading . . .</p>
        </div>
    );
};