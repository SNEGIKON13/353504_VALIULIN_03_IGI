import * as ActionTypes from './ActionTypes';

/* Set reducer to handle redux state */
export const profileImages = (state = { 
    isLoading: true,
    errMess: null,
    profile_images:[]}, action) => {
    switch (action.type) {
        case ActionTypes.ADD_PROFILE_IMAGES:
            return {...state, isLoading: false, errMess: null, profile_images: action.payload};

        case ActionTypes.PROFILE_IMAGES_LOADING:
            return {...state, isLoading: true, errMess: null, profile_images: []}

        case ActionTypes.PROFILE_IMAGES_FAILED:
            return {...state, isLoading: false, errMess: action.payload};

        default:
            return state;
    }
};