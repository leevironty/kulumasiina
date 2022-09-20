import { writable, type Writable } from "svelte/store";

export interface Msg {
  msg: string;
  status: null | 'success' | 'danger';
}

let timeoutId: ReturnType<typeof setTimeout>;

export const msg: Writable<Msg> = writable({msg: '', status: null});

export const setMsg = (newMsg: Msg) => {
  msg.set(newMsg);
  clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    msg.set({status: null, msg: ''});
  }, 5000)
}