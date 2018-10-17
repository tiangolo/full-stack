import { Store } from 'vuex';

import { State, setToken, setLoggedIn } from '@/store';
import { api } from '@/api';


export const checkGetToken = (store: Store<State>) => {
    if (store.state.token) {
        return store.state.token;
    } else {
        const token = localStorage.getItem('token');
        if (token) {
            store.commit(setToken, token);
        }
        return token || '';
    }
};

export const checkIsLoggedIn = async (store: Store<State>) => {
    if (store.state.isLoggedIn) {
        return true;
    } else {
        const token = checkGetToken(store);
        if (token) {
            const loggedIn = await api.getMe(token).then((response) => {
                store.commit(setLoggedIn, true);
                return true;
            }).catch((err) => {
                removeToken();
                store.commit(setToken, '');
                return false;
            });
            return loggedIn;
        } else {
            store.commit(setLoggedIn, false);
            return false;
        }
    }
};

export const saveToken = (token: string) => localStorage.setItem('token', token);

export const removeToken = () => localStorage.removeItem('token');
