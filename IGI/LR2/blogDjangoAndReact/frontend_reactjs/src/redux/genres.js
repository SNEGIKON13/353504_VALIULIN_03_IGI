import * as ActionTypes from './ActionTypes';

/* Set reducer to handle redux state */
export const Genres = (state = { 
    isLoading: true,
    errMess: null,
    genres:[]}, action) => {
    switch (action.type) {
        case ActionTypes.ADD_GENRES:
            return {...state, isLoading: false, errMess: null, genres: action.payload};

        case ActionTypes.GENRES_LOADING:
            return {...state, isLoading: true, errMess: null, genres: []}

        case ActionTypes.GENRES_FAILED:
            return {...state, isLoading: false, errMess: action.payload};

        default:
            return state;
    }
};