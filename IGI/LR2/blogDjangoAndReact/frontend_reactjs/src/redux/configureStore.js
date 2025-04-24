import {createStore, combineReducers, applyMiddleware} from 'redux';
import { createForms } from 'react-redux-form';
import { Genres } from './genres';
import { Posts } from './posts';
import { FeaturedPosts } from './featuredPosts';
import { Comments } from './comments';
import { UserData } from './userData';
import { profileImages } from './profileImages';
import { InitialComment } from './forms';
import thunk from 'redux-thunk';
import logger from 'redux-logger';
import { Auth } from './auth';

/* Configure store for letting the data be there even if the page is reloaded */
export const ConfigureStore = () => {
    const store = createStore(
        combineReducers({
            genres: Genres,
            posts: Posts,
            featuredposts: FeaturedPosts,
            comments: Comments,
            auth: Auth,
            user_data: UserData,
            profile_images: profileImages,
            ...createForms({
                comment: InitialComment
            })
        }),
        applyMiddleware(thunk, logger)
    );

    return store;
}