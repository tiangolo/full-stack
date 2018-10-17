import axios from 'axios';

import { apiUrl } from '@/env';

const logInGetToken = async (username: string, password: string) => {
    return axios.post(`${apiUrl}/api/v1/login/access-token`, {
      username,
      password,
    });
};

const getMe = async (token: string) => {
  return axios.get(`${apiUrl}/api/v1/users/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const api = {
    logInGetToken,
    getMe,
};
