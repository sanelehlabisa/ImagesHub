import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent {
  signInForm: FormGroup = new FormGroup({});

  emailRegex: string = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$";

  constructor(private router: Router, private userService: UserService) {}

  ngOnInit(): void {
    this.signInForm = new FormGroup({
      email: new FormControl("", [
        Validators.required, 
        Validators.pattern(this.emailRegex)
      ])
    });
  }

  get email() {
    return this.signInForm.get('email');
  }

  signIn(): void {
    this.userService.signIn(this.email?.value).subscribe({
      next: (user) => {
        this.userService.setUser(user); // Use the setUser method to update the signal
        let routerUrl: string = user.type ? "images" : "requests";
        this.router.navigate([`/user/browse-${routerUrl}`]);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }
}
