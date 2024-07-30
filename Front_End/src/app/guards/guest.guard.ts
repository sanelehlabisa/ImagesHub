import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';

export const guestGuard: CanActivateFn = (route, state) => {
  const userService = inject(UserService);
  const router = inject(Router);

  const user = userService.getUser();
  
  if (user && user.type === 1) {
    return true;
  } else {
    router.navigate(['/sign-in']);
    return false;
  }
};