import * as ActionTypes from './ActionTypes';

/* Set reducer to handle redux state */
export const UserData = (state = { 
    isLoading: true,
    errMess: null,
    user_data:[]}, action) => {
    switch (action.type) {
        case ActionTypes.ADD_USER_DATA:
            return {...state, isLoading: false, errMess: null, user_data: action.payload};

        case ActionTypes.USER_DATA_LOADING:
            return {...state, isLoading: true, errMess: null, user_data: []}

        case ActionTypes.USER_DATA_FAILED:
            return {...state, isLoading: false, errMess: action.payload};

        default:
            return state;
    }
};