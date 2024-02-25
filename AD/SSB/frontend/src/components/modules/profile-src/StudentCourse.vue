<template>
  <div class="course-block">
    <p>{{ dep }}</p>
    <a href="#" @click="goTo()">{{ title }}</a>
    <div class='right-arrow'>
      <ul>
        <li>
          <a class='animated-arrow' href='#' @click="goTo()">
        <span class='the-arrow -left'>
          <span class='shaft'></span>
        </span>
            <span class='main'>
          <span class='text'>
            Перейти
          </span>
          <span class='the-arrow -right'>
            <span class='shaft'></span>
          </span>
        </span>
          </a>
        </li>
      </ul>
    </div>

  </div>
</template>

<script>
import CourseView from "@/components/common/CourseView";

export default {
  name: "StudentCourse",
  props: {
    title: String,
    courseId: Number,
    dep: String
  },
  methods: {
    goTo: function (){
      this.$store.state.viewCourseId = this.courseId;
      this.$store.commit("change_module", CourseView);
    }
  }
}
</script>

<style lang="scss" scoped>
.course-block {
  width: 100%;
  border: 1px solid rgba(255, 255, 255, .524);
  margin-top: 15px;
  background-color: #2c3e50;
}

.course-block * {
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-start;
}

.right-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  margin-top: -35px;
}

.right-arrow * {
  position: relative;
  align-self: flex-end;
  margin-right: 20px;
}

// Variables

$black: #4c4c4c;
$white: #eaeaea;
$gray: #808080;

$text-arrow-space: 16px;
$shaft-width: 1px;
$newshaft-width: 64px;
$shaft-thickness: 1px;
$arrow-head-width: 8px;
$arrow-head-thickness: $shaft-thickness;

// Base

* {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

html,
body {
  background: #ffffff;
  height: 100%;
  font-family: "Helvetica Neue LT W01_41488878";
  font-size: 16px;
  line-height: 26px;
}

.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

ul {
  li {
    margin: 0 0 24px;
  }
}

// The Arrow

.the-arrow {
  width: $shaft-width;
  transition: all 0.2s;

  &.-left {
    position: absolute;
    top: 60%;
    left: 0;

    > .shaft {
      width: 0;
      background-color: $white;

      &:before,
      &:after {
        width: 0;
        background-color: $white;
      }

      &:before {
        transform: rotate(0);
      }

      &:after {
        transform: rotate(0);
      }
    }
  }

  &.-right {
    top: 3px;

    > .shaft {
      width: $shaft-width;
      transition-delay: 0.2s;

      &:before,
      &:after {
        width: $arrow-head-width;
        transition-delay: 0.3s;
        transition: all 0.5s;
      }

      &:before {
        transform: rotate(40deg);
      }

      &:after {
        transform: rotate(-40deg);
      }
    }
  }

  > .shaft {
    background-color: $black;
    display: block;
    height: $shaft-thickness;
    position: relative;
    transition: all 0.2s;
    transition-delay: 0;
    will-change: transform;

    &:before,
    &:after {
      background-color: $black;
      content: "";
      display: block;
      height: $arrow-head-thickness;
      position: absolute;
      top: 0;
      right: 0;
      transition: all 0.2s;
      transition-delay: 0;
    }

    &:before {
      transform-origin: top right;
    }

    &:after {
      transform-origin: bottom right;
    }
  }
}

// Animated Arrow Button

.animated-arrow {
  display: inline-block;
  color: $black;
  font-size: 1.25em;
  font-style: italic;
  text-decoration: none;
  position: relative;
  transition: all 0.2s;

  &:hover {
    color: $white;

    > .the-arrow.-left {
      > .shaft {
        width: $newshaft-width;
        transition-delay: 0.1s;
        background-color: $white;

        &:before,
        &:after {
          width: $arrow-head-width;
          transition-delay: 0.1s;
          background-color: $white;
        }

        &:before {
          transform: rotate(40deg);
        }

        &:after {
          transform: rotate(-40deg);
        }
      }
    }

    > .main {
      transform: translateX($shaft-width + $text-arrow-space);
      transform: translateX($newshaft-width + $text-arrow-space);

      > .the-arrow.-right {
        > .shaft {
          width: 0;
          transform: translateX(200%);
          transition-delay: 0;

          &:before,
          &:after {
            width: 0;
            transition-delay: 0;
            transition: all 0.1s;
          }

          &:before {
            transform: rotate(0);
          }

          &:after {
            transform: rotate(0);
          }
        }
      }
    }
  }

  > .main {
    display: flex;
    align-items: center;
    transition: all 0.2s;

    > .text {
      margin: 0 $text-arrow-space 0 0;
      line-height: 1;
    }

    > .the-arrow {
      position: relative;
    }
  }

}

</style>