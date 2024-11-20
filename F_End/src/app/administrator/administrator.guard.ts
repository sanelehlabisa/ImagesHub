import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

export const administratorGuard: CanActivateFn = (route, state) => {
  const userService = inject(UserService);
  const router = inject(Router);

  const user = userService.getSignedInUser();
  if (userService.isAuthenticated(1)) {
    return true;
  } else {
    router.navigate(['/']);
    return false;
  }
};